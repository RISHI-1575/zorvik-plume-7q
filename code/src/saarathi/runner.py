"""Run a scenario under a chosen controller and collect safety/trip metrics."""
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import traci

from .config import SCENARIO_DIR, RESULTS_DIR, STEP_LENGTH_S, HALT_SPEED
from .controllers import load_controller

FRONT_ROW_M = 8.0        # stop-line zone for the filtering check
SAMPLE_EVERY_S = 10
# ponytail: replay keeps minutes 5-15 at 1 Hz (~5 MB JSON); widen once it is streamed/binary.
REPLAY_FROM_S, REPLAY_TO_S = 300, 900
_SUB = (traci.constants.VAR_POSITION, traci.constants.VAR_ANGLE, traci.constants.VAR_SPEED)


class Replay:
    """Vehicle positions + signal states for the browser replay, and a full-run queue series."""

    def __init__(self, path: Path, tls_ids):
        import sumolib
        net = sumolib.net.readNet(str(SCENARIO_DIR / 'corridor.net.xml'))
        r = lambda p: [round(p[0], 1), round(p[1], 1)]
        self.path, self.tls_ids = path, tls_ids
        self.out = {
            'from': REPLAY_FROM_S, 'to': REPLAY_TO_S, 'types': [], 'vtype': [],
            'roads': [{'pts': [r(p) for p in e.getShape()], 'lanes': e.getLaneNumber(), 'name': e.getName()}
                      for e in net.getEdges()],
            'nodes': [[r(p) for p in n.getShape()] for n in net.getNodes() if len(n.getShape()) > 2],
            'tls': [], 'approaches': [], 'frames': [],
            'series': {'t': [], 'queue': [], 'running': [], 'arrived': []}}
        self.lanes = []      # per approach: incoming lanes, for halting counts
        for tls in tls_ids:
            by = {}
            for i, link in enumerate(traci.trafficlight.getControlledLinks(tls)):
                if link:
                    a = by.setdefault(traci.lane.getEdgeID(link[0][0]), {'links': [], 'lanes': set()})
                    a['links'].append(i)
                    a['lanes'].add(link[0][0])
            node = None
            for edge, a in by.items():
                e = net.getEdge(edge)
                (x0, y0), (x1, y1) = e.getShape()[-2:]
                node = node or e.getToNode().getCoord()
                self.out['approaches'].append({'tls': tls, 'name': e.getName(), 'links': a['links'],
                                               'pos': r((x1, y1)), 'dir': r((x1 - x0, y1 - y0))})
                self.lanes.append(sorted(a['lanes']))
            self.out['tls'].append({'id': tls, 'pos': r(node) if node else None})
        self.vid, self.arrived = {}, 0

    def _track(self, ids):
        types = self.out['types']
        for v in ids:
            t = traci.vehicle.getTypeID(v)
            if not any(x['id'] == t for x in types):
                types.append({'id': t, 'len': traci.vehicletype.getLength(t),
                              'wid': traci.vehicletype.getWidth(t)})
            self.vid[v] = len(self.out['vtype'])
            self.out['vtype'].append(next(i for i, x in enumerate(types) if x['id'] == t))
            traci.vehicle.subscribe(v, _SUB)

    def step(self, t: float) -> None:
        self.arrived += traci.simulation.getArrivedNumber()
        sec = int(round(t))
        if sec == REPLAY_FROM_S:
            self._track(traci.vehicle.getIDList())
        elif REPLAY_FROM_S < sec < REPLAY_TO_S:
            self._track(traci.simulation.getDepartedIDList())
        if REPLAY_FROM_S <= sec < REPLAY_TO_S:
            P, A, S = _SUB
            flat = []
            for v, d in traci.vehicle.getAllSubscriptionResults().items():
                if v in self.vid and P in d:
                    x, y = d[P]
                    flat += [self.vid[v], round(x * 10), round(y * 10), round(d[A]), round(d[S] * 10)]
            self.out['frames'].append({'v': flat, 's': [traci.trafficlight.getRedYellowGreenState(x)
                                                        for x in self.tls_ids]})
        elif sec == REPLAY_TO_S:
            for v in traci.vehicle.getIDList():
                if v in self.vid:
                    traci.vehicle.unsubscribe(v)
        if sec % SAMPLE_EVERY_S == 0:
            s = self.out['series']
            s['t'].append(sec)
            s['queue'].append([sum(traci.lane.getLastStepHaltingNumber(l) for l in ls) for ls in self.lanes])
            s['running'].append(traci.vehicle.getIDCount())
            s['arrived'].append(self.arrived)

    def save(self) -> None:
        import json
        self.path.write_text(json.dumps(self.out, separators=(',', ':')))


def run(controller: str, sim_seconds: int, seed: int = 0, gui: bool = False,
        label: str | None = None, profile: str | None = None, routes=None,
        replay: Path | None = None) -> dict:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    label = label or f'{controller}_s{seed}'
    tripinfo = RESULTS_DIR / f'tripinfo_{label}.xml'

    name = 'sumo-gui' if gui else 'sumo'
    # pip-installed sumo lives next to the interpreter even when .venv/bin is not on PATH
    binary = shutil.which(name) or shutil.which(name, path=str(Path(sys.executable).parent))
    if not binary:
        raise FileNotFoundError(f'{name} not found on PATH or in {Path(sys.executable).parent}')
    extra = ['--route-files', str(routes)] if routes else []
    if profile:
        vtypes = SCENARIO_DIR / f'vtypes_{profile}.add.xml'
        if not vtypes.exists():
            raise FileNotFoundError(f'{vtypes} missing: rebuild the scenario')
        extra += ['--additional-files', str(vtypes)]
    traci.start([binary, '-c', str(SCENARIO_DIR / 'corridor.sumocfg'), *extra,
                 '--tripinfo-output', str(tripinfo),
                 '--tripinfo-output.write-unfinished', 'true',
                 '--seed', str(seed),
                 '--device.emissions.probability', '1',   # CO2/fuel in tripinfo (HBEFA default classes)
                 '--no-warnings',
                 '--quit-on-end'])
    safety = {'collisions': 0, 'teleports': 0, 'emergency_stops': 0}
    crashed = set()   # with collision.action=warn an overlap is re-reported every step
    unfinished = 0
    front = {'bike': 0, 'all': 0}
    try:
        tls_ids = list(traci.trafficlight.getIDList())
        cls = load_controller(controller)
        ctrls = [cls(tls) for tls in tls_ids]
        rec = Replay(replay, tls_ids) if replay else None
        t = 0.0
        while traci.simulation.getMinExpectedNumber() > 0 and t < sim_seconds:
            traci.simulationStep()
            t += STEP_LENGTH_S
            # Teleport/emergency counters are per-step events; collisions are
            # counted once per (collider, victim) pair. On-junction ones are
            # SUMO's optional shape-overlap check, reported separately.
            crashed.update((c.collider, c.victim, c.lane.startswith(':'))
                           for c in traci.simulation.getCollisions())
            safety['teleports'] += traci.simulation.getStartingTeleportNumber()
            if hasattr(traci.simulation, 'getEmergencyStoppingVehiclesNumber'):
                safety['emergency_stops'] += (
                    traci.simulation.getEmergencyStoppingVehiclesNumber())
            for c in ctrls:
                c.step(t, STEP_LENGTH_S)
            if int(t) % SAMPLE_EVERY_S == 0:
                _sample_front_row(tls_ids, front)
            if rec:
                rec.step(t)
        unfinished = traci.simulation.getMinExpectedNumber()
        if rec:
            rec.save()
        safety['junction_collisions'] = sum(j for *_, j in crashed)
        safety['collisions'] = len(crashed) - safety['junction_collisions']
    finally:
        traci.close()
    m = parse_tripinfo(tripinfo) | safety | {'unfinished_vehicles': unfinished}
    # never-inserted vehicles have no tripinfo record, so they are invisible to delay_s
    m['insertion_backlog'] = max(0, unfinished - (m['vehicles'] - m['completed_trips']))
    m['front_row_bike_share'] = front['bike'] / front['all'] if front['all'] else 0.0
    return m


def _sample_front_row(tls_ids, front) -> None:
    """Realism check: who is stopped at the stop line on red approaches.

    Indian mixed traffic: two-wheelers filter to the front, so the bike share
    in the first FRONT_ROW_M should exceed the bike modal share.
    """
    for tls in tls_ids:
        state = traci.trafficlight.getRedYellowGreenState(tls)
        red = {link[0][0] for i, link in
               enumerate(traci.trafficlight.getControlledLinks(tls))
               if link and state[i] in 'rs'}
        for lane in red:
            stop = traci.lane.getLength(lane) - FRONT_ROW_M
            for v in traci.lane.getLastStepVehicleIDs(lane):
                if (traci.vehicle.getLanePosition(v) >= stop
                        and traci.vehicle.getSpeed(v) < HALT_SPEED):
                    front['all'] += 1
                    front['bike'] += traci.vehicle.getTypeID(v) == 'bike'


def parse_tripinfo(path: Path) -> dict:
    root = ET.parse(path).getroot()
    trips = root.findall('tripinfo')
    n = len(trips)
    if n == 0:
        return {
            'vehicles': 0,
            'completed_trips': 0,
            'depart_delay_s': 0.0,
            'delay_incl_depart_s': 0.0,
            'stops_per_veh': 0.0,
            'delay_s': 0.0,
            'travel_time_s': 0.0,
            'waiting_s': 0.0,
            'bike_share': 0.0,
        }
    mean = lambda attr: sum(float(x.get(attr)) for x in trips) / n
    loss = sorted(float(x.get('timeLoss')) for x in trips)
    by = {}
    for x in trips:
        by.setdefault(x.get('vType'), []).append(float(x.get('timeLoss')))
    em = [e for e in (x.find('emissions') for x in trips) if e is not None]
    return {
        'delay_p95_s': loss[min(n - 1, int(0.95 * n))],
        'delay_by_class': {k: sum(v) / len(v) for k, v in by.items()},
        'co2_kg': sum(float(e.get('CO2_abs', 0)) for e in em) / 1e6,      # mg -> kg
        'fuel_l': sum(float(e.get('fuel_abs', 0)) for e in em) / 745e3,   # mg -> litres, petrol density

        'vehicles': n,
        # unfinished vehicles are written with delay truncated at sim end, so
        # delay_s under-states gridlock: read it beside completed_trips.
        'completed_trips': sum(float(x.get('arrival')) >= 0 for x in trips),
        'depart_delay_s': mean('departDelay'),
        'delay_incl_depart_s': mean('timeLoss') + mean('departDelay'),
        'stops_per_veh': mean('waitingCount'),
        'delay_s': mean('timeLoss'),
        'travel_time_s': mean('duration'),
        'waiting_s': mean('waitingTime'),
        'bike_share': sum(x.get('vType') == 'bike' for x in trips) / n,
    }
