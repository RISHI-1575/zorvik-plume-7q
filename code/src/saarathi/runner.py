"""Run a scenario under a chosen controller and collect safety/trip metrics."""
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import traci

from .config import SCENARIO_DIR, RESULTS_DIR, STEP_LENGTH_S
from .controllers import CONTROLLERS

def run(controller: str, sim_seconds: int, seed: int = 0, gui: bool = False,
        label: str | None = None) -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    label = label or f'{controller}_s{seed}'
    tripinfo = RESULTS_DIR / f'tripinfo_{label}.xml'

    binary = shutil.which('sumo-gui' if gui else 'sumo')
    traci.start([binary, '-c', str(SCENARIO_DIR / 'corridor.sumocfg'),
                 '--tripinfo-output', str(tripinfo),
                 '--tripinfo-output.write-unfinished', 'true',
                 '--seed', str(seed),
                 '--no-warnings',
                 '--quit-on-end'])
    safety = {'collisions': 0, 'teleports': 0, 'emergency_stops': 0}
    unfinished = 0
    try:
        tls_ids = list(traci.trafficlight.getIDList())
        ctrls = [CONTROLLERS[controller](tls) for tls in tls_ids]
        t = 0.0
        while traci.simulation.getMinExpectedNumber() > 0 and t < sim_seconds:
            traci.simulationStep()
            t += STEP_LENGTH_S
            # These TraCI counters describe events starting in this step, so
            # accumulating them does not repeatedly count queued vehicles.
            safety['collisions'] += len(traci.simulation.getCollisions())
            safety['teleports'] += traci.simulation.getStartingTeleportNumber()
            if hasattr(traci.simulation, 'getEmergencyStoppingVehiclesNumber'):
                safety['emergency_stops'] += (
                    traci.simulation.getEmergencyStoppingVehiclesNumber())
            for c in ctrls:
                c.step(t, STEP_LENGTH_S)
        unfinished = traci.simulation.getMinExpectedNumber()
    finally:
        traci.close()
    return parse_tripinfo(tripinfo) | safety | {'unfinished_vehicles': unfinished}


def parse_tripinfo(path: Path) -> dict:
    root = ET.parse(path).getroot()
    trips = root.findall('tripinfo')
    n = len(trips)
    if n == 0:
        return {
            'vehicles': 0,
            'stops_per_veh': 0.0,
            'delay_s': 0.0,
            'travel_time_s': 0.0,
            'waiting_s': 0.0,
        }
    mean = lambda attr: sum(float(x.get(attr)) for x in trips) / n
    return {
        'vehicles': n,
        'stops_per_veh': mean('waitingCount'),
        'delay_s': mean('timeLoss'),
        'travel_time_s': mean('duration'),
        'waiting_s': mean('waitingTime'),
    }
