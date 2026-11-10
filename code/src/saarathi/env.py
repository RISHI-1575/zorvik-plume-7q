"""SaarathiHubEnv — Gymnasium environment for ONE self-learning junction.

The agent controls junction J2's signal (through the SafetyShell — it cannot
act unsafely). Other junctions run max-pressure. State includes time-of-day,
so the hub can learn the junction's daily rhythm (IDEA.md §2).

Observation (all normalized):
  [ queue PCU per incoming approach (4),
    one-hot of current green phase (n_greens),
    time-in-green / MAX_GREEN,
    sin(time-of-day), cos(time-of-day),
    weekday flag ]
Action: Discrete(n_greens) — request that green phase (shell may defer it).
Reward: -(total queue PCU)/100  - 0.5 * switch penalty
"""
import math
import shutil

import gymnasium as gym
import numpy as np
import traci

from . import demand
from .config import (SCENARIO_DIR, STEP_LENGTH_S, MAX_GREEN_S,
                     DECISION_INTERVAL_S, SCENARIO)
from .controllers import MaxPressure, SafetyShell
from .pcu import lane_queue_pcu

RL_TLS = SCENARIO.junction_ids[min(1, len(SCENARIO.junction_ids) - 1)]
OTHER_TLS = [tls for tls in SCENARIO.junction_ids if tls != RL_TLS]
QUEUE_NORM = 40.0  # PCU that counts as "very congested" per approach
REFERENCE_APPROACHES = 4
REFERENCE_GREENS = 2
REFERENCE_OBS_DIM = REFERENCE_APPROACHES + REFERENCE_GREENS + 4


class SaarathiHubEnv(gym.Env):
    metadata = {'render_modes': []}

    def __init__(self, hours=(8, 10), weekday=True, seed_base=0, gui=False):
        self.hours = hours
        self.weekday = weekday
        self.seed_base = seed_base
        self.gui = gui
        self.episode = 0
        self.sim_seconds = (hours[1] - hours[0]) * 3600
        self._started = False
        self.observation_space = gym.spaces.Box(-1.0, 2.0,
                                                shape=(REFERENCE_OBS_DIM,),
                                                dtype=np.float32)
        self.action_space = gym.spaces.Discrete(REFERENCE_GREENS)

    # ------------------------------------------------------------ lifecycle
    def _start_sumo(self, seed: int):
        demand.generate(hours=self.hours, seed=seed)
        binary = shutil.which('sumo-gui' if self.gui else 'sumo')
        traci.start([binary, '-c', str(SCENARIO_DIR / 'corridor.sumocfg'),
                     '--seed', str(seed), '--quit-on-end', '--no-warnings'])
        self.shell = SafetyShell(RL_TLS)
        self.others = [MaxPressure(t) for t in OTHER_TLS]
        self.in_lanes = sorted({l[0][0] for l in
                                traci.trafficlight.getControlledLinks(RL_TLS) if l})
        self.approaches = sorted({l.rsplit('_', 1)[0] for l in self.in_lanes})
        n_greens = len(self.shell.greens)
        obs_dim = len(self.approaches) + n_greens + 4
        if (len(self.approaches), n_greens, obs_dim) != (
                REFERENCE_APPROACHES, REFERENCE_GREENS, REFERENCE_OBS_DIM):
            raise RuntimeError(
                "SaarathiHubEnv currently targets the reference 4-arm, "
                "2-green junction. Build a manifest-driven observation adapter "
                "before training on a different signal layout."
            )
        self.t = 0.0
        self._started = True

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        if self._started:
            traci.close()
        self.episode += 1
        self._start_sumo(self.seed_base + self.episode)
        # warm up: 60s under the shell's initial green before first decision
        for _ in range(60):
            self._sim_step()
        return self._obs(), {}

    # ---------------------------------------------------------------- steps
    def _sim_step(self):
        traci.simulationStep()
        self.t += STEP_LENGTH_S
        self.shell.step(STEP_LENGTH_S)
        for c in self.others:
            c.step(self.t, STEP_LENGTH_S)

    def step(self, action: int):
        prev_green = self.shell.current_green
        self.shell.request(self.shell.greens[int(action)])
        for _ in range(int(DECISION_INTERVAL_S / STEP_LENGTH_S)):
            self._sim_step()
        queue = sum(lane_queue_pcu(l) for l in self.in_lanes)
        switched = self.shell.current_green != prev_green
        reward = -queue / 100.0 - (0.5 if switched else 0.0)
        terminated = (traci.simulation.getMinExpectedNumber() == 0
                      or self.t >= self.sim_seconds)
        return self._obs(), reward, terminated, False, {'queue_pcu': queue}

    # ----------------------------------------------------------------- obs
    def _obs(self):
        q = [min(sum(lane_queue_pcu(l) for l in self.in_lanes
                     if l.startswith(app + '_')) / QUEUE_NORM, 2.0)
             for app in self.approaches]
        onehot = [1.0 if g == self.shell.current_green else 0.0
                  for g in self.shell.greens]
        tod = (self.hours[0] * 3600 + self.t) / 86400 * 2 * math.pi
        obs = q + onehot + [
            min(self.shell.time_in_green / MAX_GREEN_S, 1.0),
            math.sin(tod), math.cos(tod),
            1.0 if self.weekday else 0.0,
        ]
        return np.asarray(obs, dtype=np.float32)

    def close(self):
        if self._started:
            traci.close()
            self._started = False
