"""Template for testing YOUR signal algorithm on any Saarathi scenario.

    python run.py --scenario scenarios/old_airport_road/corridor.yaml \
                  --controller examples/my_controller.py:LongestQueue

Contract: the runner builds Class(tls_id) once per traffic light and calls
step(t, dt) every simulation step. Use raw TraCI for observations; send phase
choices through SafetyShell.request() so min-green, yellow and all-red stay
guaranteed (the shell ignores illegal requests). RL agents fit the same
contract: load the policy in __init__, call it in step().
"""
import traci

from saarathi.controllers import SafetyShell
from saarathi.pcu import lane_queue_pcu


class LongestQueue:
    """Serve the green phase with the largest PCU-weighted queue."""

    def __init__(self, tls_id: str, every_s: float = 5.0):
        self.shell = SafetyShell(tls_id)
        self.every_s, self._next = every_s, 0.0

    def step(self, t: float, dt: float) -> None:
        self.shell.step(dt)
        if t < self._next:
            return
        self._next = t + self.every_s
        queue = {g: sum(lane_queue_pcu(i) for i, _ in self.shell.served_links(g))
                 for g in self.shell.greens}
        best = max(queue, key=queue.get)
        if self.shell.must_rotate() and best == self.shell.current_green:
            best = max((g for g in queue if g != best), key=queue.get, default=best)
        self.shell.request(best)
