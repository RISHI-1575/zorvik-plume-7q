# Saarathi — Code

Open Indian mixed-traffic environment plus Saarathi's decentralised traffic-signal controller. Final definition: [../PROJECT_DEFINITION.md](../PROJECT_DEFINITION.md) · Active plan: [../FINAL_PLAN.md](../FINAL_PLAN.md) · Older design notes are archived.

## Setup (once)
```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt      # installs SUMO 1.27 via pip wheels too
./.venv/bin/python scenarios/build_corridor.py   # build the 4-junction corridor
```

## Run
```bash
export PATH="$PWD/.venv/bin:$PATH"               # so sumo/netconvert are found

./.venv/bin/python run.py --controller fixed --hours 8 9        # fixed-time baseline
./.venv/bin/python run.py --controller maxp  --hours 8 9        # max-pressure baseline
./.venv/bin/python run.py --controller maxp  --hours 8 9 --gui  # watch it
./.venv/bin/python run.py --compare --hours 8 10 --seeds 5      # results_v2.csv -> experiments/results/
./.venv/bin/python verify.py                                    # rebuild + unit tests + clean smoke run
./.venv/bin/python summarize_results.py --last 9                # presentation summary from final run
```

## Train the hub (Phase 3)
```bash
./.venv/bin/pip install stable-baselines3 torch
./.venv/bin/python train_hub.py --steps 100000
./.venv/bin/python train_hub.py --eval models/hub_J2.zip --gui
```

## Layout
```
scenarios/build_corridor.py   4-junction Bengaluru-style corridor (sublane = lane-less)
scenarios/corridor4/corridor.yaml  authoritative scenario manifest (junctions, traffic, vehicles, PCU)
src/saarathi/config.py        PCU values (IRC), safety limits, daily demand profile
src/saarathi/demand.py        time-of-day route generation (the daily rhythm)
src/saarathi/pcu.py           PCU-weighted sensing (one mixed flow, no discrimination)
src/saarathi/controllers.py   SafetyShell + FixedTime + MaxPressure
src/saarathi/runner.py        simulation runner + tripinfo metrics
src/saarathi/env.py           SaarathiHubEnv — Gymnasium env for the RL hub (J2)
run.py                        experiment CLI
train_hub.py                  PPO training / evaluation
```

## First results (sanity check — AM peak 8-9, seed 0)
| controller | vehicles | stops/veh | delay (s) | travel time (s) | waiting (s) |
|---|---|---|---|---|---|
| fixed-time | 4162 | 2.0 | 66.5 | 138.9 | 42.3 |
| max-pressure | 4179 | 2.2 | **46.4 (−30%)** | 118.9 | **20.4 (−52%)** |

Pipeline verified: adaptive control beats fixed-time as expected. The hub must now beat max-pressure (IMPLEMENTATION.md, week-17 gate).

## Demo status

`corridor4` is a configurable **synthetic reference scenario**, not a calibrated Bengaluru corridor. Its node count, demand, vehicle classes and PCU baseline are declared in `scenarios/corridor4/corridor.yaml`. Before making paper-grade claims, follow [../SIMULATOR_RESEARCH_AND_BUILD_PLAN.md](../SIMULATOR_RESEARCH_AND_BUILD_PLAN.md): field counts, calibration and held-out validation are required.
