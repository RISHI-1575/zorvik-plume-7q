# Saarathi — Code

Open Indian mixed-traffic environment plus Saarathi's decentralised traffic-signal controller. Final definition: [../PROJECT_DEFINITION.md](../PROJECT_DEFINITION.md) · Active plan: [../FINAL_PLAN.md](../FINAL_PLAN.md) · Older design notes are archived.

## Setup (once)
```bash
cd code
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt      # SUMO 1.27 itself comes as a pip wheel (eclipse-sumo)
./.venv/bin/python scenarios/build_corridor.py   # build the 4-junction corridor
```
To watch runs in the SUMO window (`sumo-gui`) on macOS, install XQuartz once, then log out and back in:
```bash
brew install --cask xquartz
```

## Saarathi Studio (the simulator, in the browser)
```bash
export PATH="$PWD/.venv/bin:$PATH"
python studio.py                                  # open http://127.0.0.1:8765
```
A three-column control room: settings on the left, the junction replay in the middle, readings on the right.

1. **Pick a place** (left): a Bengaluru junction from the list ("ready" means it is already
   built), **Choose on map**, or **Draw your own area** on that map (max 4 km²). An unbuilt
   place is downloaded from OpenStreetMap and turned into a left-hand, lane-less SUMO network
   the first time you run it (about a minute).
2. **Pick a time** of day (the bars show the daily traffic curve), then press **Run simulation**.
   Every run tests four systems on the same seeds: the **Current plan** (the stored signal
   program, the baseline), **Fixed timer**, **Sensor timer** (actuated) and **Smart signal** (max-pressure).
3. **Watch** (centre): roads with names, signal heads and vehicles coloured by type replay
   minutes 5–15 of seed 0. Switch between the four systems or **Side by side** (Fixed vs Smart). Drag to pan,
   scroll to zoom, press Space to play or pause. The strip below shows each approach's signal timeline.
4. **Read** (right): first, **How effective was each system?**: each system's delay vs the
   current plan, how many repeats it won on identical traffic, safety events, and a verdict.
   *Better*/*Worse* needs a win/loss in every repeat (all but one with 8+); anything else is
   *No clear difference*. Below that, Fixed vs Smart in detail: the delay headline, p95, stops, trip time, fuel and CO₂ (HBEFA-modelled,
   provisional), what the change means for commuters, the simulation checks (collisions,
   teleports, unfinished vehicles), queue and completed-trip charts, the longest queues by road,
   delay by vehicle type, every repeat, and **All numbers** with the CSV.
5. **Advanced** (optional): amount of traffic (100% = the busiest signal at capacity; default
   60%; lower it if roads jam) and repeats (default 5). **Past runs** (header) reopens earlier
   results (`experiments/studio_runs/`). Runs made before replays existed show numbers only.

Use 5 seeds for any number you report (RULES.md). 1 or 3 seeds are for quick looks only.

## Command line
```bash
export PATH="$PWD/.venv/bin:$PATH"               # so sumo/netconvert are found

python scenarios/make_area.py --name hsr --bbox 12.905 77.630 12.918 77.645   # any OSM area (S W N E)
S=scenarios/silk_board/corridor.yaml
python run.py --scenario $S --compare --controllers fixed,maxp --seeds 5 --hours 9 10 --demand 0.8 --jobs 4
python run.py --scenario $S --controller maxp --hours 9 10 --demand 0.8 --gui  # watch it
python run.py --controller fixed --hours 8 9                    # synthetic 4-junction corridor
python verify.py                                                # rebuild + unit tests + clean smoke run
python summarize_results.py --input experiments/results/<area>/results_v6.csv                          # presentation summary from final run
```
`--demand` scales `entering_veh_per_hour`. `--jobs` runs SUMO in parallel. `--json` also
writes the rows as JSON. Results are appended to
`experiments/results/<scenario>/results_v5.csv`.

## Real corridor: HAL Old Airport Road (OSM + BTP) and your own algorithm
```bash
S=scenarios/old_airport_road/corridor.yaml
bash scenarios/old_airport_road/fetch_osm.sh                    # once: OSM -> osm.net.xml (+ buildings)
SAARATHI_SCENARIO=$S python scenarios/build_corridor.py         # BTP cycles + behaviour profiles
python run.py --scenario $S --controller program --hours 8 9    # the signal plan the road runs (BTP cycle)
python run.py --scenario $S --controller examples/my_controller.py:LongestQueue
python run.py --scenario $S --compare --seeds 5 --profile lane_disciplined   # behaviour ablation
python render_sumo.py --scenario $S --focus isro                # overview.png + junction GIF
```
Your controller: any class `C(tls_id)` with `step(t, dt)`; route phase changes
through `SafetyShell` (see `examples/my_controller.py`). Results go to
`experiments/results/old_airport_road/results_v5.csv`, with collisions (lane,
and on-junction shape overlaps separately), teleports and
`front_row_bike_share` (realism check) always reported.
Status: geometry and BTP cycles are sourced; demand, phase splits and behaviour
are provisional (`../docs/assumptions.md` A-005..A-013). Not a calibrated model.

## Compared with the 2012 heterogeneous-traffic work
| | IISc, Anusha, Verma & Kavitha (ASCE JTE 139(5); received May 2012) | SiMTraM, IIT Bombay (SUMO 0.12, 2013) | Saarathi Studio |
|-|-|-|-|
| What it is | Field study plus an equation: saturation flow at Bangalore signals vs two-wheeler share | Lane-less mixed-traffic patch for SUMO 0.12 | Simulator and test bench on SUMO 1.27 |
| Area | A few Bangalore intersections | Powai (Mumbai) screenshots; validated later (2016) on Ahmedabad | Any Bengaluru area up to 4 km², drawn on a map, built from OSM |
| Vehicle mix | Two-wheeler share as a factor | Bike, cycle, rickshaw, car, HGV, bus | Bike, auto, car, LCV, bus, truck with IRC:106 PCUs and the Bengaluru 2022 modal split (Basu et al.) |
| Lane-less behaviour | n/a (measured) | Lane split into strips | SUMO sublane model, 0.4 m; two-wheelers filter to the stop line (front-row bike share measured) |
| Signal algorithms | n/a | n/a | Plug in any Python controller; compare it against fixed-time, actuated and max-pressure on the same seeds |
| Safety output | n/a | not reported | Lane collisions, junction overlaps, teleports and emergency stops for every run |
| Time of day | Peak observations | n/a | 24-hour demand profile; pick any hour |
| Open / runnable today | Paper (paywalled) | GPLv3 source, known segfaults on large networks | Open source, one command, runs on a laptop |

What the 2012 study has and Saarathi does not yet have: **field measurements**.
Saarathi's demand and behaviour are provisional (`docs/assumptions.md`). The next
step is to calibrate saturation flow against Anusha et al.'s Bangalore
observations, and travel speed against the TomTom rush-hour speed (13.9 km/h).
The other ~2012 IISc simulation could not be found (`docs/data_sources.md` §6).

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
studio.py, studio/index.html  Saarathi Studio (stdlib web server + one-page UI)
scenarios/make_area.py        OSM area -> runnable scenario (signals named by street)
user_controllers/             algorithms uploaded through the Studio
train_hub.py                  PPO training / evaluation
```

## First results (sanity check — AM peak 8-9, seed 0)
| controller | vehicles | stops/veh | delay (s) | travel time (s) | waiting (s) |
|---|---|---|---|---|---|
| fixed-time | 4162 | 2.0 | 66.5 | 138.9 | 42.3 |
| max-pressure | 4179 | 2.2 | **46.4 (−30%)** | 118.9 | **20.4 (−52%)** |

Pipeline verified: adaptive control beats fixed-time as expected. The hub must now beat max-pressure (IMPLEMENTATION.md, week-17 gate).

## Map-area results (5 seeds, hour 9-10, demand 0.6)
Delay in s, mean ± std across seeds 0-4. Full rows: `experiments/results/<area>/results_v5.csv`, summaries: `baseline_summary.csv`.

| area | fixed-time | actuated | max-pressure |
|---|---|---|---|
| Domlur | 217.8 ± 133.1 | 164.0 ± 122.6 | **152.2 ± 77.2** |
| Silk Board | 32.2 ± 4.8 | 34.8 ± 1.1 | **29.5 ± 7.8** |

Lesson: on seed 0 alone, fixed-time (126 s) looked better than max-pressure (271 s) on Domlur. Across 5 seeds the ranking flips — fixed-time has two near-gridlock seeds (350 s, 376 s) while max-pressure is the most stable and has the fewest junction overlaps (42 vs 90 mean). This is why RULES.md requires 5 seeds for any reported number.

## Demo status

`corridor4` is a configurable **synthetic reference scenario**, not a calibrated Bengaluru corridor. Its node count, demand, vehicle classes and PCU baseline are declared in `scenarios/corridor4/corridor.yaml`. Before making paper-grade claims, follow [../SIMULATOR_RESEARCH_AND_BUILD_PLAN.md](../SIMULATOR_RESEARCH_AND_BUILD_PLAN.md): field counts, calibration and held-out validation are required.
