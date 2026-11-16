#!/usr/bin/env python
"""Summarise a results CSV: one row per (scenario, profile, hours, demand, controller), mean ± SD over seeds."""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parent
METRICS = [
    "delay_s", "travel_time_s", "waiting_s", "stops_per_veh",
    "collisions", "teleports", "unfinished_vehicles",
    # v6+ columns; absent in older CSVs (reported as blank, not 0)
    "completed_trips", "insertion_backlog", "depart_delay_s", "delay_incl_depart_s",
]
RUN_KEY = ("scenario", "profile", "hours", "demand", "controller", "seed")
GROUP_KEY = ("scenario", "profile", "hours", "demand", "controller")


def latest_per_run(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    """Keep the last row per run key (re-runs overwrite earlier ones); return (rows, dropped)."""
    keep = {tuple(r.get(k, "") for k in RUN_KEY): r for r in rows}
    return list(keep.values()), len(rows) - len(keep)


def provenance() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip() or "nogit"
    except OSError:
        sha = "nogit"
    return f"# git {sha} | python {' '.join(sys.argv)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or args.input.with_name("baseline_summary.csv")

    with args.input.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows, dropped = latest_per_run(rows)
    if dropped:
        print(f"note: {dropped} duplicate run rows replaced by their latest re-run")
    grouped: dict[tuple, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row.get(k, "") for k in GROUP_KEY), []).append(row)

    out_rows = []
    for key in sorted(grouped):
        group = grouped[key]
        summary = dict(zip(GROUP_KEY, key)) | {"seeds": len(group)}
        for metric in METRICS:
            if any(row.get(metric) in (None, "") for row in group):
                summary[f"{metric}_mean"] = summary[f"{metric}_sd"] = ""
                continue
            values = [float(row[metric]) for row in group]
            summary[f"{metric}_mean"] = mean(values)
            summary[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0
        out_rows.append(summary)

    fields = list(out_rows[0])
    with output.open("w", newline="") as handle:
        handle.write(provenance() + "\n")
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"wrote {output}")
    for row in out_rows:
        print(
            f"{row['profile']:>14} d{row['demand']:<4} {row['controller']:>8} n={row['seeds']}  delay {row['delay_s_mean']:.1f} ± "
            f"{row['delay_s_sd']:.1f}s  waiting {row['waiting_s_mean']:.1f} ± "
            f"{row['waiting_s_sd']:.1f}s  collisions {row['collisions_mean']:.1f}"
        )


if __name__ == "__main__":
    main()
