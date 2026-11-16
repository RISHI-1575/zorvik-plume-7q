#!/usr/bin/env python
"""Saarathi experiment CLI.

Examples:
  python run.py --controller fixed --hours 8 10          # AM peak, fixed-time
  python run.py --controller actuated --hours 8 10       # gap-based baseline
  python run.py --controller maxp  --hours 8 10 --gui    # watch max-pressure
  python run.py --compare --hours 8 10 --seeds 3         # baseline table

Real Bengaluru corridor (OSM + BTP cycles) and your own controller:
  python run.py --scenario scenarios/old_airport_road/corridor.yaml --controller program
  python run.py --scenario ... --controller examples/my_controller.py:LongestQueue
  python run.py --scenario ... --compare --seeds 5 --profile lane_disciplined
"""
import argparse
import csv
import os
import sys
from pathlib import Path

# The scenario must be chosen before saarathi.config loads the manifest.
if '--scenario' in sys.argv:
    os.environ['SAARATHI_SCENARIO'] = str(
        Path(sys.argv[sys.argv.index('--scenario') + 1]).resolve())
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from saarathi import demand
from saarathi.config import RESULTS_DIR, SCENARIO
from saarathi.controllers import CONTROLLERS
from saarathi.runner import run

COLS = [
    'vehicles', 'stops_per_veh', 'delay_s', 'travel_time_s', 'waiting_s',
    'collisions', 'junction_collisions', 'teleports', 'emergency_stops', 'unfinished_vehicles',
    'bike_share', 'front_row_bike_share',
    'completed_trips', 'insertion_backlog', 'depart_delay_s', 'delay_incl_depart_s',
]


def one(controller, hours, seed, gui=False, profile=None, scale=1.0, replay=None):
    tag = controller.split(':')[-1] if ':' in controller else controller
    replay = Path(f'{replay}.{tag}.replay.json') if replay else None
    label = f'{tag}_{profile or "active"}_h{hours[0]}-{hours[1]}_d{scale:g}_s{seed}'
    # Per-run route file so parallel runs never overwrite each other's demand.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    routes = demand.generate(hours=tuple(hours), seed=seed, scale=scale,
                             out=RESULTS_DIR / f'routes_{label}.rou.xml')
    try:
        m = run(controller, sim_seconds=(hours[1] - hours[0]) * 3600, seed=seed,
                gui=gui, profile=profile, label=label, routes=routes, replay=replay)
    finally:
        routes.unlink(missing_ok=True)
    m |= {'controller': tag, 'seed': seed, 'hours': f'{hours[0]}-{hours[1]}',
          'scenario': SCENARIO.name, 'profile': profile or 'active', 'demand': scale}
    return m


def _one(job):
    return one(*job)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario', help='path to a corridor.yaml manifest')
    ap.add_argument('--controller', default='fixed',
                    help=f'{"/".join(CONTROLLERS)} or module:Class / file.py:Class')
    ap.add_argument('--profile', help='behaviour profile from the manifest')
    ap.add_argument('--hours', nargs=2, type=int, default=[8, 10],
                    metavar=('FROM', 'TO'), help='window of the daily profile')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--seeds', type=int, help='run N seeds (with --compare)')
    ap.add_argument('--compare', action='store_true',
                    help='run all controllers and print a table')
    ap.add_argument('--controllers', help='comma list to compare (default: all built-ins)')
    ap.add_argument('--demand', type=float, default=1.0,
                    help='demand scale: 1.0 = manifest entering_veh_per_hour (for map areas: estimated capacity)')
    ap.add_argument('--jobs', type=int, default=1, help='parallel SUMO runs')
    ap.add_argument('--json', help='also write rows as JSON here')
    ap.add_argument('--gui', action='store_true')
    ap.add_argument('--replay', help='write seed 0 replays to PREFIX.<controller>.replay.json')
    args = ap.parse_args()
    if args.hours[1] <= args.hours[0]:
        ap.error("TO must be greater than FROM")

    if args.compare:
        names = args.controllers.split(',') if args.controllers else list(CONTROLLERS)
        jobs = [(c, args.hours, s, False, args.profile, args.demand, args.replay if s == 0 else None)
                for c in names for s in range(args.seeds or 1)]
    else:
        jobs = [(args.controller, args.hours, args.seed, args.gui, args.profile, args.demand, args.replay)]
    rows = []
    if args.jobs > 1 and len(jobs) > 1:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(args.jobs) as ex:
            for r in ex.map(_one, jobs):
                print(f'done {r["controller"]} seed {r["seed"]}', flush=True)
                rows.append(r)
    else:
        for j in jobs:
            print(f'... running {j[0]} seed {j[2]}', flush=True)
            rows.append(_one(j))
            print(f'done {j[0]} seed {j[2]}', flush=True)
    if args.json:
        import json
        Path(args.json).write_text(json.dumps(rows, default=str))

    hdr = ['controller', 'seed'] + COLS
    print('\n' + '  '.join(f'{h:>14}' for h in hdr))
    for r in rows:
        print('  '.join(f'{r.get(h, ""):>14.1f}' if isinstance(r.get(h), float)
                        else f'{str(r.get(h, "")):>14}' for h in hdr))

    # Versioned schema (never append to an older header): v3 added
    # scenario/profile/realism, v4 deduplicated collisions + junction_collisions.
    # v5 added the demand column. v6 added throughput + depart-delay columns.
    out = RESULTS_DIR / 'results_v6.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ['scenario', 'profile', 'hours', 'demand'] + hdr
    write_header = not out.exists()
    with out.open('a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if write_header:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})
    print(f'\nappended -> {out}')


if __name__ == '__main__':
    main()
