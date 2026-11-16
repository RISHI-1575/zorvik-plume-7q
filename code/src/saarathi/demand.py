"""Generate routes.rou.xml for a time window of the daily profile.

Flows follow HOURLY_PROFILE (the junction's daily rhythm) and the Bengaluru
modal split. Deterministic given a seed, so experiments are reproducible.
"""
import random
from pathlib import Path

from .config import (SCENARIO, SCENARIO_DIR, HOURLY_PROFILE, PEAK_FLOWS,
                     MODAL_SPLIT, N_JUNCTIONS)


def _streams():
    """(name, list-of-edges, peak veh/h) for every origin-destination stream."""
    chain_e = [f'W0_J1'] + [f'J{i}_J{i+1}' for i in range(1, N_JUNCTIONS)] + [f'J{N_JUNCTIONS}_E{N_JUNCTIONS+1}']
    chain_w = [f'E{N_JUNCTIONS+1}_J{N_JUNCTIONS}'] + [f'J{i+1}_J{i}' for i in reversed(range(1, N_JUNCTIONS))] + ['J1_W0']
    yield 'main_we', chain_e, PEAK_FLOWS['main_through']
    yield 'main_ew', chain_w, PEAK_FLOWS['main_through']
    for i in range(1, N_JUNCTIONS + 1):
        yield f'side_ns_{i}', [f'N{i}_J{i}', f'J{i}_S{i}'], PEAK_FLOWS['side_through']
        yield f'side_sn_{i}', [f'S{i}_J{i}', f'J{i}_N{i}'], PEAK_FLOWS['side_through']
    # turning streams: side road -> arterial east, arterial west -> side road
    for i in range(1, N_JUNCTIONS + 1):
        rest_e = chain_e[i:] if i < len(chain_e) else []
        yield f'turn_in_{i}', [f'N{i}_J{i}'] + rest_e, PEAK_FLOWS['turn']
        yield f'turn_out_{i}', chain_e[:i] + [f'J{i}_S{i}'], PEAK_FLOWS['turn']


def generate(hours=(8, 10), seed=0, out: Path | None = None,
             scale: float = 1.0) -> Path:
    """Write flows for sim time 0..(hours span), applying the hourly profile."""
    rng = random.Random(seed)
    out = out or SCENARIO_DIR / 'routes.rou.xml'
    if SCENARIO.is_osm:
        return _generate_osm(hours, seed, out, scale)
    lines = ['<routes>']
    fid = 0
    for h in range(hours[0], hours[1]):
        mult = HOURLY_PROFILE[h % 24] * scale
        begin = (h - hours[0]) * 3600
        end = begin + 3600
        for name, edges, peak in _streams():
            for vtype, share in MODAL_SPLIT.items():
                vph = peak * mult * share
                if vph < 1:
                    continue
                lines.append(
                    f'  <flow id="f{fid}_{name}_{vtype}_h{h}" type="{vtype}" '
                    f'begin="{begin}" end="{end}" vehsPerHour="{vph:.1f}" '
                    f'route="!route" departLane="best" departSpeed="max" '
                    f'departPosLat="random"/>'.replace(
                        'route="!route"',
                        f'route="r{fid}"'))
                lines.insert(1, f'  <route id="r{fid}" edges="{" ".join(edges)}"/>')
                fid += 1
    lines.append('</routes>')
    out.write_text('\n'.join(lines))
    return out


def _generate_osm(hours, seed, out: Path, scale: float) -> Path:
    """Real-network demand: randomTrips + duarouter, one batch per hour.

    Fringe-weighted so most trips enter/leave at the network edge and run
    along the corridor; the class is sampled from the `mix` vTypeDistribution
    (modal split). ponytail: no OD matrix yet; swap for routeSampler on field
    counts once they exist (calibration gate).
    """
    import os, subprocess, sys, tempfile
    import xml.etree.ElementTree as ET
    import sumo
    tool = os.path.join(os.path.dirname(sumo.__file__), 'tools', 'randomTrips.py')
    rate = float(SCENARIO.traffic['entering_veh_per_hour'])
    vehicles = []
    with tempfile.TemporaryDirectory() as tmp:
        for h in range(hours[0], hours[1]):
            vph = rate * HOURLY_PROFILE[h % 24] * scale
            begin = (h - hours[0]) * 3600
            rou = Path(tmp) / f'h{h}.rou.xml'
            subprocess.run([
                sys.executable, tool, '-n', str(SCENARIO_DIR / 'corridor.net.xml'),
                '-a', str(SCENARIO_DIR / 'vtypes.add.xml'),
                '-b', str(begin), '-e', str(begin + 3600),
                '--insertion-rate', f'{vph:.1f}', '--random-depart',
                '--fringe-factor', '20', '--min-distance', '1500',
                # prefer arterials: free-flow shortest paths rat-run through 1-lane service roads and gridlock (A-013)
                '--duarouter-weights.priority-factor', '5',
                '--seed', str(seed * 100 + h), '--prefix', f'h{h}_',
                '-t', 'type="mix" departLane="best" departSpeed="max" departPosLat="random"',
                '-o', str(Path(tmp) / f'h{h}.trips.xml'), '-r', str(rou)],
                check=True, capture_output=True)
            vehicles += ET.parse(rou).getroot().findall('vehicle')
    root = ET.Element('routes')
    root.extend(sorted(vehicles, key=lambda v: float(v.get('depart'))))
    ET.ElementTree(root).write(out, encoding='UTF-8', xml_declaration=True)
    return out


if __name__ == '__main__':
    p = generate()
    print('routes written:', p)
