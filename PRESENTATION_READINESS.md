# Saarathi — Presentation Readiness (2026-11-10)

## What is ready to demonstrate

> **A configurable SUMO prototype for Indian-style mixed traffic, with PCU-aware sensing, a hard traffic-signal safety shell, and three working controller baselines.**

### Live demonstration flow

1. Open `code/scenarios/corridor4/corridor.yaml`.
   - Explain that the node count, vehicle types, traffic mix, PCU factors and geometry are now declared in one place.
   - State clearly: this is a synthetic reference corridor, not yet a calibrated Bengaluru corridor.
2. Run `python verify.py`.
   - It rebuilds the scenario, executes five scenario-contract tests and runs a one-hour PCU Max-Pressure smoke test.
   - The checked run completes 4,320 trips with zero collisions and zero teleports.
3. Run `python run.py --compare --hours 8 9 --seeds 3`.
   - Compare fixed-time, actuated and PCU Max-Pressure with identical demand and seeds.
4. Run `python train_hub.py --steps 512`.
   - Show that the PPO environment initializes, runs, and writes a model. Do not evaluate or claim this short model is trained, safe or superior.

## Verified results: 08:00–09:00 synthetic AM-peak reference scenario

| Controller | Seeds | Mean delay (s) | Mean waiting (s) | Interpretation |
|---|---:|---:|---:|---|
| Fixed-time | 3 | 69.4 | 44.0 | Basic timing baseline |
| Actuated | 3 | 70.4 | 46.1 | Local gap-based baseline; needs parameter tuning |
| PCU Max-Pressure | 3 | 46.5 | 21.0 | Strongest current controller in this synthetic prototype |

The PCU Max-Pressure run recorded **zero collisions and zero teleports across all three final seeds**. Fixed-time and actuated each had one collision in the three-seed comparison; the safety counters deliberately expose this rather than hiding it. No paper claim should be made from these synthetic results.

## What to say when asked about the real system

- “We have completed the simulator prototype and benchmark harness.”
- “The reference corridor is configurable; four nodes are a current test instance, not the project limit.”
- “PCU values are versioned in the scenario and will be field-calibrated; we do not treat them as universal.”
- “Our next validation gate is field-count calibration and held-out testing on a Bengaluru corridor.”

## Do not claim tomorrow

- that it is a calibrated Bengaluru digital twin;
- that Saarathi beats real BATCS;
- that the short PPO model is trained;
- that the current synthetic setting proves real-world congestion reduction;
- that no earlier Indian mixed-traffic simulator exists.

## Commands

```bash
cd "/Users/rishi/Personal/final year project/Saarathi/code"
export PATH="$PWD/.venv/bin:$PATH"

python verify.py
python run.py --compare --hours 8 9 --seeds 3
python summarize_results.py --input experiments/results/<area>/results_v7.csv
python train_hub.py --steps 512
```
