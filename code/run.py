#!/usr/bin/env python
"""Saarathi experiment CLI.

Examples:
  python run.py --controller fixed --hours 8 10          # AM peak, fixed-time
  python run.py --controller actuated --hours 8 10       # gap-based baseline
  python run.py --controller maxp  --hours 8 10 --gui    # watch max-pressure
  python run.py --compare --hours 8 10 --seeds 3         # baseline table
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from saarathi import demand
from saarathi.config import RESULTS_DIR
from saarathi.runner import run

CONTROLLERS = ['fixed', 'actuated', 'maxp']
COLS = [
    'vehicles', 'stops_per_veh', 'delay_s', 'travel_time_s', 'waiting_s',
    'collisions', 'teleports', 'emergency_stops', 'unfinished_vehicles',
]


def one(controller, hours, seed, gui=False):
    demand.generate(hours=tuple(hours), seed=seed)
    m = run(controller, sim_seconds=(hours[1] - hours[0]) * 3600,
            seed=seed, gui=gui, label=f'{controller}_h{hours[0]}-{hours[1]}_s{seed}')
    m |= {'controller': controller, 'seed': seed, 'hours': f'{hours[0]}-{hours[1]}'}
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--controller', choices=CONTROLLERS, default='fixed')
    ap.add_argument('--hours', nargs=2, type=int, default=[8, 10],
                    metavar=('FROM', 'TO'), help='window of the daily profile')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--seeds', type=int, help='run N seeds (with --compare)')
    ap.add_argument('--compare', action='store_true',
                    help='run all controllers and print a table')
    ap.add_argument('--gui', action='store_true')
    args = ap.parse_args()
    if args.hours[1] <= args.hours[0]:
        ap.error("TO must be greater than FROM")

    rows = []
    if args.compare:
        for c in CONTROLLERS:
            for s in range(args.seeds or 1):
                print(f'... running {c} seed {s}')
                rows.append(one(c, args.hours, s))
    else:
        rows.append(one(args.controller, args.hours, args.seed, gui=args.gui))

    hdr = ['controller', 'seed'] + COLS
    print('\n' + '  '.join(f'{h:>14}' for h in hdr))
    for r in rows:
        print('  '.join(f'{r.get(h, ""):>14.1f}' if isinstance(r.get(h), float)
                        else f'{str(r.get(h, "")):>14}' for h in hdr))

    # Keep the original early prototype CSV intact. This versioned schema adds
    # safety metrics, so appending it to the old header would silently corrupt
    # column alignment.
    out = RESULTS_DIR / 'results_v2.csv'
    write_header = not out.exists()
    with out.open('a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['hours'] + hdr)
        if write_header:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in ['hours'] + hdr})
    print(f'\nappended -> {out}')


if __name__ == '__main__':
    main()
