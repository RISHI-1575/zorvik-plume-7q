"""Signal controllers: safety shell, fixed-time, actuated and max-pressure.

The SafetyShell is the non-negotiable layer: ANY controller (rule-based or RL)
can only *request* a green phase; the shell enforces min/max green, yellow and
all-red clearance. The learned agent physically cannot make the signal unsafe.
"""
import traci

from .config import (MIN_GREEN_S, MAX_GREEN_S, YELLOW_S, ALL_RED_S,
                     DECISION_INTERVAL_S)
from .pcu import lane_queue_pcu


class SafetyShell:
    """Wraps one traffic light. Exposes green phases; executes safe switches."""

    def __init__(self, tls_id: str):
        self.tls = tls_id
        logic = traci.trafficlight.getAllProgramLogics(tls_id)[0]
        self.phases = logic.phases
        # green phases = those with at least one 'G' and no 'y'
        self.greens = [i for i, p in enumerate(self.phases)
                       if 'G' in p.state and 'y' not in p.state]
        # yellow phase that follows each green in the program (netconvert layout)
        self.yellow_after = {g: (g + 1) % len(self.phases) for g in self.greens}
        self.n_links = len(self.phases[0].state)
        self.current_green = self.greens[0]
        self.time_in_green = 0.0
        self._pending = None          # target green during a transition
        self._transition_left = 0.0
        self._stage = None            # 'yellow' | 'allred'
        traci.trafficlight.setPhase(tls_id, self.current_green)
        traci.trafficlight.setPhaseDuration(tls_id, 10_000)  # we own timing

    # ---- links served by a green phase: [(in_lane, out_lane), ...]
    def served_links(self, green: int):
        state = self.phases[green].state
        links = traci.trafficlight.getControlledLinks(self.tls)
        return [(l[0][0], l[0][1]) for i, l in enumerate(links)
                if l and state[i] in 'Gg']

    def request(self, target_green: int) -> None:
        """Ask to move to target_green. Ignored unless legal right now."""
        if self._pending is not None or target_green == self.current_green:
            return
        if self.time_in_green < MIN_GREEN_S:
            return
        self._pending = target_green
        self._stage = 'yellow'
        self._transition_left = YELLOW_S
        traci.trafficlight.setPhase(self.tls, self.yellow_after[self.current_green])
        traci.trafficlight.setPhaseDuration(self.tls, 10_000)

    def must_rotate(self) -> bool:
        return self.time_in_green >= MAX_GREEN_S

    @property
    def is_transitioning(self) -> bool:
        return self._pending is not None

    def step(self, dt: float) -> None:
        if self._pending is None:
            self.time_in_green += dt
            return
        self._transition_left -= dt
        if self._transition_left > 0:
            return
        if self._stage == 'yellow':
            self._stage = 'allred'
            self._transition_left = ALL_RED_S
            traci.trafficlight.setRedYellowGreenState(self.tls, 'r' * self.n_links)
        else:  # all-red done -> enter target green
            self.current_green = self._pending
            self._pending, self._stage = None, None
            self.time_in_green = 0.0
            # setRedYellowGreenState installed a temporary 1-phase override
            # program; restore the base program before selecting the phase.
            traci.trafficlight.setProgram(self.tls, '0')
            traci.trafficlight.setPhase(self.tls, self.current_green)
            traci.trafficlight.setPhaseDuration(self.tls, 10_000)


class FixedTime:
    """Today's signal: rotate greens on a fixed cycle, ignore traffic."""

    def __init__(self, tls_id: str, green_s: float = 30.0):
        self.shell = SafetyShell(tls_id)
        self.green_s = green_s

    def step(self, t: float, dt: float) -> None:
        self.shell.step(dt)
        if self.shell.time_in_green >= self.green_s:
            greens = self.shell.greens
            nxt = greens[(greens.index(self.shell.current_green) + 1) % len(greens)]
            self.shell.request(nxt)


class Actuated:
    """Local gap-based baseline using vehicles detected on served approaches.

    The controller holds the current green while traffic is present.  Once the
    minimum green has elapsed, it changes phase after a short detection gap if
    another phase has demand.  The safety shell still owns every transition.
    """

    def __init__(self, tls_id: str, gap_s: float = 3.0):
        self.shell = SafetyShell(tls_id)
        self.gap_s = gap_s
        self._gap = 0.0
        self._next_decision = 0.0

    def _demand(self, green: int) -> int:
        incoming = {i for i, _ in self.shell.served_links(green)}
        return sum(traci.lane.getLastStepVehicleNumber(lane)
                   for lane in incoming)

    def step(self, t: float, dt: float) -> None:
        self.shell.step(dt)
        if self.shell.is_transitioning:
            self._gap = 0.0
            return

        current_demand = self._demand(self.shell.current_green)
        self._gap = 0.0 if current_demand else self._gap + dt
        if t < self._next_decision:
            return
        self._next_decision = t + DECISION_INTERVAL_S

        scores = {g: self._demand(g) for g in self.shell.greens}
        alternatives = {g: n for g, n in scores.items()
                        if g != self.shell.current_green}
        if not alternatives:
            return
        best_other = max(alternatives, key=alternatives.get)
        should_switch = (
            self.shell.must_rotate()
            or (self._gap >= self.gap_s and alternatives[best_other] > 0)
        )
        if should_switch:
            self.shell.request(best_other)


class MaxPressure:
    """PCU-weighted max-pressure: serve the movement with most waiting pressure.

    The strong classical baseline every learned method must beat.
    """

    def __init__(self, tls_id: str):
        self.shell = SafetyShell(tls_id)
        self._next_decision = 0.0

    def _pressure(self, green: int) -> float:
        return sum(lane_queue_pcu(i) - lane_queue_pcu(o)
                   for i, o in self.shell.served_links(green))

    def step(self, t: float, dt: float) -> None:
        self.shell.step(dt)
        if t < self._next_decision:
            return
        self._next_decision = t + DECISION_INTERVAL_S
        scores = {g: self._pressure(g) for g in self.shell.greens}
        best = max(scores, key=scores.get)
        if self.shell.must_rotate() and best == self.shell.current_green:
            others = {g: s for g, s in scores.items() if g != best}
            if others:
                best = max(others, key=others.get)
        self.shell.request(best)


CONTROLLERS = {
    'fixed': FixedTime,
    'actuated': Actuated,
    'maxp': MaxPressure,
}
