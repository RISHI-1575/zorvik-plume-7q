"""Turn any OpenStreetMap area into a runnable Saarathi scenario.

    python scenarios/make_area.py --name silk_board --bbox 12.911 77.617 12.923 77.629

bbox is south west north east (degrees). Downloads roads, signals and
buildings from the Overpass API (ODbL, (c) OpenStreetMap contributors), builds
a left-hand SUMO net, names every signal by its streets, writes corridor.yaml
(behaviour, PCU and vehicle classes copied from the Old Airport Road template)
and runs build_corridor.py. Needs sumo/netconvert on PATH.
"""
import argparse
import copy
import datetime as dt
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'old_airport_road' / 'corridor.yaml'
OVERPASS = 'https://overpass-api.de/api/interpreter'
MAX_KM2 = 4.0
ROADS = 'trunk|trunk_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link'
# Demand 1.0 = throughput of the busiest signal: its incoming lanes x
# saturation flow x (1 - lost time) / number of green phases. Fringe-lane
# capacity overestimated Silk Board 3.5x and gridlocked it. Provisional
# (docs/assumptions.md A-013).
SAT_FLOW_PCU_PER_LANE_H = 1800
EFFECTIVE_GREEN = 0.85
# Urban Bengaluru roadside counts 2022 (Basu et al., J. Road Safety 37(2);
# docs/data_sources.md section 1). Sourced, not junction-specific.
MODAL_SPLIT_2022 = {'bike': 0.365, 'auto': 0.082, 'car': 0.406, 'lcv': 0.054,
                    'bus': 0.050, 'truck': 0.043}


def area_km2(s, w, n, e):
    import math
    return (n - s) * 111.32 * (e - w) * 111.32 * math.cos(math.radians((n + s) / 2))


def fetch_osm(bbox, out: Path):
    s, w, n, e = bbox
    q = (f'[out:xml][timeout:120];('
         f'way["highway"~"^({ROADS})$"]({s},{w},{n},{e});'
         f'node["highway"="traffic_signals"]({s},{w},{n},{e});'
         f'way["building"]({s},{w},{n},{e}););(._;>;);out body;')
    req = urllib.request.Request(OVERPASS, data=urllib.parse.urlencode({'data': q}).encode(),
                                 headers={'User-Agent': 'saarathi-studio/0.1'})
    with urllib.request.urlopen(req, timeout=180) as r:
        out.write_bytes(r.read())
    print(f'osm: {out.stat().st_size // 1024} kB from Overpass', flush=True)


def build_net(d: Path, bbox):
    s, w, n, e = bbox
    subprocess.run([
        'netconvert', '--osm-files', 'area.osm', '-o', 'osm.net.xml', '--lefthand', 'true',
        '--keep-edges.by-type', ','.join('highway.' + t for t in ROADS.split('|')),
        '--keep-edges.in-geo-boundary', f'{w},{s},{e},{n}',
        '--remove-edges.by-vclass', 'pedestrian,rail,tram', '--keep-edges.components', '1',
        '--geometry.remove', '--ramps.guess', '--roundabouts.guess', '--junctions.join',
        '--tls.guess-signals', '--tls.discard-simple', '--tls.join', '--tls.default-type', 'static',
        '--no-turnarounds', '--output.street-names', '--osm.sidewalks', 'false', '--edges.join',
        '--ignore-errors.edge-type', '--no-warnings'], cwd=d, check=True)
    import sumo
    typ = Path(sumo.__file__).parent / 'data' / 'typemap' / 'osmPolyconvert.typ.xml'
    subprocess.run(['polyconvert', '--osm-files', 'area.osm', '--net-file', 'osm.net.xml',
                    '--type-file', str(typ), '-o', 'buildings.poly.xml',
                    '--ignore-errors', '--no-warnings'], cwd=d, check=True)
    print('net: osm.net.xml + buildings.poly.xml', flush=True)


def signals_and_capacity(net_file: Path, template: dict):
    """Name signals by their streets; busiest-signal throughput (veh/h) = demand 1.0."""
    import sumolib
    net = sumolib.net.readNet(str(net_file), withPrograms=True)
    signals, caps = {}, [0.0]
    for tls in net.getTrafficLights():
        lanes = {c[0].getID() for c in tls.getConnections()}
        phases = next(iter(tls.getPrograms().values())).getPhases()
        greens = sum(1 for p in phases if 'y' not in p.state and 'G' in p.state.upper())
        caps.append(len(lanes) * SAT_FLOW_PCU_PER_LANE_H * EFFECTIVE_GREEN / max(greens, 1))
        names = sorted({c[0].getEdge().getName() for c in tls.getConnections()} - {''})
        base = re.sub(r'[^a-z0-9]+', '_', ' x '.join(names[:2]).lower()).strip('_') or 'signal'
        key, i = base, 2
        while key in signals:
            key, i = f'{base}_{i}', i + 1
        signals[key] = tls.getID()
    entry_lanes = sum(e.getLaneNumber() for e in net.getEdges() if not e.getIncoming())
    pcu = template['pcu']['factor_sets'][template['pcu']['active']]['factors']
    mean_pcu = sum(pcu[v] * s for v, s in MODAL_SPLIT_2022.items())
    return signals, entry_lanes, round(max(caps) / mean_pcu, -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True, help='scenario id: lowercase letters, digits, _')
    ap.add_argument('--bbox', nargs=4, type=float, required=True, metavar=('S', 'W', 'N', 'E'))
    args = ap.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,40}', args.name):
        ap.error('name must be a lowercase slug')
    s, w, n, e = args.bbox
    if not (s < n and w < e):
        ap.error('bbox must be south west north east')
    if area_km2(*args.bbox) > MAX_KM2:
        ap.error(f'area {area_km2(*args.bbox):.1f} km2 > {MAX_KM2} km2: pick a smaller area')

    d = HERE / args.name
    d.mkdir(exist_ok=True)
    if not (d / 'area.osm').exists():
        fetch_osm(args.bbox, d / 'area.osm')
    build_net(d, args.bbox)

    tmpl = yaml.safe_load(TEMPLATE.read_text())
    signals, lanes, cap = signals_and_capacity(d / 'osm.net.xml', tmpl)
    if not signals:
        sys.exit('no traffic signals in this area: pick an area with at least one signalised junction')
    m = copy.deepcopy(tmpl)
    m['name'] = args.name
    m['description'] = (f'User-selected OpenStreetMap area {args.bbox} (left-hand traffic), '
                        f'{len(signals)} signals named by their streets. Demand, phase splits '
                        'and behaviour are provisional. Not a calibrated model.')
    m['network'] = {'source': 'osm', 'raw_net_file': 'osm.net.xml', 'bbox': args.bbox,
                    'osm_date': dt.date.today().isoformat(), 'signals': signals,
                    'btp_cycle_s': {}}
    m['traffic']['entering_veh_per_hour'] = cap
    m['traffic']['modal_split'] = MODAL_SPLIT_2022
    m['traffic']['entry_lanes'] = lanes
    (d / 'corridor.yaml').write_text(
        '# Generated by scenarios/make_area.py; edit freely. Status labels: docs/assumptions.md\n'
        + yaml.safe_dump(m, sort_keys=False, width=100))
    print(f'signals: {len(signals)} ({", ".join(list(signals)[:6])}...), '
          f'entry lanes {lanes}, demand 1.0 = {cap:.0f} veh/h', flush=True)
    subprocess.run([sys.executable, str(HERE / 'build_corridor.py')], check=True,
                   env={**os.environ, 'SAARATHI_SCENARIO': str(d / 'corridor.yaml')})
    print(f'ready: {d / "corridor.yaml"}', flush=True)


if __name__ == '__main__':
    main()
