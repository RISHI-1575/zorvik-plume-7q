# Saarathi — Project Status and Publication Plan

**Updated:** 2026-11-10  
**Read with:** `PROJECT_DEFINITION.md`, `FINAL_PLAN.md`, and `LITERATURE_AUDIT.md`.

## Final project in one line

Saarathi is an open, reproducible, Bengaluru-inspired SUMO benchmark for Indian mixed/non-lane traffic, plus a safe decentralised traffic-signal reference controller that can coordinate neighbouring junctions and handle ambulance priority.

## Important positioning decision

Do **not** claim that Saarathi is the first Indian traffic simulator, the first Indian traffic-signal RL system, the first PCU-aware controller, the first green-wave controller, or the first ambulance-recovery system.

Existing work includes IIT Bombay's SiMTraM, Indian heterogeneous/PCU RL studies, MARL communication methods, and emergency-pre-emption/recovery studies. Saarathi's defensible contribution is a **field-informed, open, reproducible evaluation scenario and protocol**, with a transparent reference controller.

## How to make publication likely

The single biggest upgrade is **field-informed calibration**.

1. Collect manual/video counts at 2–3 Bengaluru junctions at morning peak, midday, and evening peak.
2. Record vehicle mix, turning movements, flow by approach, queues/discharge flow, and signal phase timings.
3. Compare real and simulated modal split, flow, queues/discharge, and travel time where possible.
4. Release the anonymised counts, SUMO files, assumptions, route generator, seeds, controller settings, and raw result CSVs.
5. Run fixed-time, actuated, tuned Max-Pressure, and Saarathi under the identical protocol for at least 5 seeds; report mean and uncertainty.
6. Make the central research question: **how do controller conclusions change when Indian mixed, weak-lane-discipline traffic is modelled explicitly?**
7. Obtain a transportation-faculty review of calibration and an ML/RL-faculty review of experimental fairness before submitting.

## Paper-safe claim

> We release a reproducible, Bengaluru-inspired SUMO benchmark that makes Indian heterogeneous and weak-lane-discipline traffic assumptions explicit, and use it to compare traffic-signal controllers under a common protocol.

## Current progress assessment

Percentages measure completed, verified work—not planned work.

| Workstream | Weight | Current state | Completion |
|---|---:|---|---:|
| Scenario/environment | 25% | Manifest-driven synthetic corridor, mixed vehicle classes, sublane setting, demand generator, and scenario-contract tests exist; field calibration remains missing. | 65% |
| Safety and PCU sensing | 10% | Versioned PCU constants and a min/max-green, yellow, all-red safety shell are implemented and smoke-tested. | 75% |
| Baselines and metrics | 15% | Fixed-time, actuated and PCU Max-Pressure run under a three-seed protocol; raw and aggregate CSV metrics are saved. External baselines and field validation are missing. | 60% |
| PPO reference controller | 15% | One-junction Gym environment and PPO training script complete a smoke run and save a model; no credible trained/evaluated RL result exists. | 25% |
| Multi-junction coordination | 10% | Not implemented. | 0% |
| Ambulance and recovery evaluation | 5% | Not implemented. | 0% |
| Reproducibility and open release | 10% | README, assumptions, manifest, verification command, raw multi-seed results and aggregate table are present; calibration data and release package are missing. | 40% |
| Paper-grade validation and writing | 10% | Project direction, version history, and literature audit exist; no calibrated study/results/paper draft. | 20% |

### Overall

- **Build completion:** approximately **45%**.
- **Paper-readiness:** approximately **18%**.
- **Core demonstrated result today:** Fixed-time, actuated and PCU Max-Pressure run in the configurable reference corridor; PCU Max-Pressure is stronger on the saved synthetic AM-peak comparison.

These numbers are intentionally conservative. A simulator existing is not the same as a credible open benchmark, and a PPO script existing is not the same as a validated learned controller.

## Next five actions, in order

1. Run the same comparison with at least five seeds and archive the raw outputs.
2. Plan the manual-count collection sheet and collect the first two junction observations.
3. Calibrate the environment and publish the calibration table before adding more AI features.
4. Train and evaluate the single-junction PPO agent against Max-Pressure on unseen seeds.
5. Add ambulance/recovery cases only after the calibration gate passes.
