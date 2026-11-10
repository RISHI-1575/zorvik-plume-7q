#!/usr/bin/env python
"""Summarise the latest controlled experiment rows into a presentation table."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "experiments" / "results" / "results_v2.csv"
METRICS = [
    "delay_s", "travel_time_s", "waiting_s", "stops_per_veh",
    "collisions", "teleports", "unfinished_vehicles",
]


def numeric(row: dict[str, str], field: str) -> float:
    return float(row[field]) if row.get(field) not in (None, "") else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--last", type=int, default=9,
                        help="number of final rows belonging to one controlled run")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "experiments" / "results" / "baseline_summary.csv")
    args = parser.parse_args()

    with args.input.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows = rows[-args.last:]
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row["controller"], []).append(row)

    out_rows = []
    for controller in sorted(grouped):
        group = grouped[controller]
        summary = {"controller": controller, "seeds": len(group)}
        for metric in METRICS:
            values = [numeric(row, metric) for row in group]
            summary[f"{metric}_mean"] = mean(values)
            summary[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0
        out_rows.append(summary)

    fields = list(out_rows[0])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"wrote {args.output}")
    for row in out_rows:
        print(
            f"{row['controller']:>8}  delay {row['delay_s_mean']:.1f} ± "
            f"{row['delay_s_sd']:.1f}s  waiting {row['waiting_s_mean']:.1f} ± "
            f"{row['waiting_s_sd']:.1f}s  collisions {row['collisions_mean']:.1f}"
        )


if __name__ == "__main__":
    main()
