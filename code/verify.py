#!/usr/bin/env python
"""One-command presentation readiness check for the Saarathi reference scenario.

This verifies the scenario manifest, rebuilds the SUMO artefacts, runs the
fast unit contracts, and executes a one-hour PCU Max-Pressure smoke run.
It is intentionally a smoke test, not a calibration or publication claim.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from saarathi import demand
from saarathi.config import SCENARIO, SCENARIO_DIR
from saarathi.runner import run

SEEPAGE_CONTRAST = 1.5   # see research/PART_A_DEEP_ANALYSIS.md F1


def main() -> None:
    print(f"Scenario: {SCENARIO.name}")
    print(f"Manifest: {SCENARIO.path}")
    print(f"Junctions: {', '.join(SCENARIO.junction_ids)}")

    subprocess.run([sys.executable, "scenarios/build_corridor.py"],
                   cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                   cwd=ROOT, check=True)

    demand.generate(hours=(8, 9), seed=0)
    metrics = run("maxp", sim_seconds=3600, seed=0,
                  label="verification_maxp_h8-9_s0")
    checks = {
        "completed trips": metrics["vehicles"] > 0,
        "no lane collisions": metrics["collisions"] == 0,
        "no teleports": metrics["teleports"] == 0,
        "no unfinished gridlock": metrics["unfinished_vehicles"] < metrics["vehicles"] * 0.1,
    }
    if "literature" in SCENARIO.profiles and "filtering" in SCENARIO.profiles:
        # Realism (RULES §3.4): the tuned default must filter clearly more than stock
        # SUMO sublane defaults ('literature') on the same seed and demand. Rate is
        # passes per bike-step spent behind a halted same-lane vehicle (congestion-neutral).
        base = run("maxp", sim_seconds=3600, seed=0, profile="literature",
                   label="verification_maxp_literature_h8-9_s0")
        ratio = metrics["seepage_rate"] / max(base["seepage_rate"], 1e-9)
        print(f"\nSeepage rate: {metrics['seepage_rate']:.4f} vs "
              f"literature {base['seepage_rate']:.4f} (x{ratio:.1f})")
        checks[f"two-wheeler seepage >= {SEEPAGE_CONTRAST}x stock SUMO"] = ratio >= SEEPAGE_CONTRAST
    print("\nVerification metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    print("\nChecks:")
    for name, passed in checks.items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
    if metrics["junction_collisions"]:
        print(f"  [WARN] {metrics['junction_collisions']} on-junction shape overlaps "
              "(SUMO --collision.check-junctions; docs/assumptions.md A-012)")
    if not all(checks.values()):
        raise SystemExit("Verification failed; do not present this run as validated.")
    print("\nPASS — reference scenario is presentation-ready as a synthetic prototype.")


if __name__ == "__main__":
    main()
