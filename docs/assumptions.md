# Saarathi Simulator Assumptions Register

Every simulator value must appear here before it is used in a paper result.

| ID | Category | Parameter | Value/range | Unit | Source/measurement | Applies to | Uncertainty | Validation status | Owner |
|---|---|---|---:|---|---|---|---|---|---|
| A-001 | PCU | Passenger car | 1.0 | PCU | Reference class | all scenarios | fixed by definition | pending | TBD |
| A-002 | PCU | Two-wheeler | TBD | PCU | IRC baseline + field calibration | reference corridor | composition-dependent | pending | TBD |
| A-003 | Geometry | Number of signal nodes | TBD | nodes | field/OSM verification | reference corridor | corridor-dependent | pending | TBD |
| A-004 | Behaviour | Lateral resolution | TBD | m | SUMO sublane calibration | reference corridor | calibration parameter | pending | TBD |
| A-005 | Geometry | Old Airport Road network (Domlur -> Doddanekundi) | 7 signals, OSM 2026-11-10 | - | OpenStreetMap API, ODbL, (c) OSM contributors; `scenarios/old_airport_road/fetch_osm.sh` | old_airport_road | lane counts/turn pockets from OSM tags, not surveyed | sourced | TBD |
| A-006 | Signals | Cycle length: Domlur 155, ISRO 193, Yamlur 100 | AM band | s | BTP published timing PDFs, `code/data/btp_signal_timings/timings.csv` (licence not stated: numbers only, PDFs not redistributed) | old_airport_road | timing date of PDFs unknown | sourced | TBD |
| A-007 | Signals | Phase split within the BTP cycle | SUMO default split scaled to cycle | s | BTP phase->approach mapping exists only in PDF diagrams | old_airport_road | high | provisional | TBD |
| A-008 | Signals | BTP junction -> OSM node mapping | by location + street names | - | manual, see corridor.yaml `signals` | old_airport_road | Wind Tunnel/Namjoshi/Doddanekundi have no BTP plan | provisional | TBD |
| A-009 | Demand | Entering trips at profile 1.0 | 3000 | veh/h | randomTrips, fringe-weighted; no OD data | old_airport_road | high; ~1.3% teleports at unsignalled side-road junctions | provisional | TBD |
| A-010 | Behaviour | Gap forcing at unsignalled junctions | impatience 0.6, jmTimegapMinor 0.5 | -, s | engineering judgement | old_airport_road `literature` profile | uncalibrated | provisional | TBD |
| A-011 | Behaviour | Lane-disciplined ablation profile | centre alignment, no sublane/pushy, minGapLat 1.5; run with `--lateral-resolution -1` (classic lane model) | - | RULES 5.6 ablation; under the sublane model queued vehicles stall mid-lane-change ±0.7 m off centre and bikes filter past them even with lcSublane 0 (2026-11-16, research/PART_A_DEEP_ANALYSIS.md F1) | old_airport_road | by construction | provisional | TBD |
| A-012 | Safety metric | Collision definition and junction geometry | `collision.mingap-factor 0` (collision = physical contact, not a minGap breach); `collision.check-junctions` on, junction shape overlaps reported separately as `junction_collisions`; each (collider, victim) pair counted once; netconvert `internal-junctions.vehicle-width` = widest class + 0.1 = 2.6 | m | SUMO docs Simulation/Safety; own tests: junction overlaps 27→8 (corridor4 seed 2), 42→15 (OAR seed 2), 3.5 m worse (215); corridor4 maxp seeds 0-4: 41-57 → 24-29/h; the one lane "collision" was a bike-bike minGap breach (0 with factor 0) | all | junction overlaps are SUMO's geometric approximation of long vehicles on curved merge paths; not field-validated | provisional | TBD |

## Status values

- `provisional`: convenient initial value, not yet sourced;
- `sourced`: supported by a cited standard/paper but not corridor-specific;
- `measured`: obtained from field observations;
- `calibrated`: fitted using the calibration dataset;
- `validated`: passed the held-out validation gate;
- `rejected`: tested and found unsuitable.

## Rule

No parameter may be described as “Indian” or “Bengaluru” merely because it appears plausible. It must be sourced, measured, calibrated or explicitly labelled provisional.
| A-013 | Demand | Demand for user-selected map areas (`make_area.py`) | demand 1.0 = busiest signal's throughput: incoming lanes × 1800 PCU/h/lane × 0.85 ÷ green phases ÷ mean PCU; modal split bike 0.365, auto 0.082, car 0.406, lcv 0.054, bus 0.050, truck 0.043; same hourly profile as OAR; routes via duarouter with `weights.priority-factor 5` (prefer arterials) | veh/h, share | split: Basu et al. 2022 (docs/data_sources.md §1); 1800 is below Indo-HCM ~2205 PCU/h/lane (conservative); 0.85 = lost-time allowance, engineering judgement | generated areas (e.g. silk_board: 1.0 = 5,140 veh/h) | no junction counts; fringe-lane capacity was tried and gridlocked Silk Board (18,770 veh/h); pure free-flow shortest paths rat-ran through 1-lane service roads and gridlocked Domlur even at demand 0.4 (priority factor 5 fixed it: Domlur fixed delay 729 s at 0.8 → 126 s at 0.6; Silk Board fixed 474 s at 0.8 → 30 s at 0.6; 1 seed each); hourly profile is not Bengaluru-sourced | provisional | TBD |
| A-014 | Behaviour | Two-wheeler filtering (`filtering` default profile) | bike: minGap 0.5, minGapLat 0.15, lcPushy 1.0, lcAssertive 5, lcSpeedGain 10, lcKeepRight 0, maxSpeedLat 1.5, lcMaxSpeedLatStanding 1.0; cars/autos/lcv/bus/truck latAlignment right; all: impatience 0.6, jmTimegapMinor 0.5 | m, -, m/s | geometry: a centred 1.8 m car in a 3.2 m lane leaves 0.7 m per side, less than a 0.75 m bike, so cars hug one edge; parameters from a 12-variant sweep, engineering judgement | silk_board, domlur, trinity, old_airport_road | seepage rate (passes per bike-step behind a halted same-lane vehicle), fixed-time, 5 seeds: Silk Board 0.8 = 0.0230 vs literature 0.0070 (3.3x), Domlur 0.6 = 0.0179 vs 0.0056 (3.2x); lane_disciplined 0; not compared with field seepage counts | provisional | TBD |
