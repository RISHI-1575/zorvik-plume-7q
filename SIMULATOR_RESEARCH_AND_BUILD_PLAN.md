# Saarathi — Indian Mixed-Traffic Simulator Research and Build Plan

**Version:** 1.0  
**Date:** 2026-11-10  
**Status:** Active plan for Part A of Saarathi  
**Priority:** Finish and validate this simulator before expanding the learning controller

---

## 1. Main goal

Build an **open, configurable and field-informed SUMO benchmark for Indian heterogeneous, weak-lane-discipline traffic at signalised urban corridors**.

The simulator must let a researcher:

1. choose or create a corridor with any practical number of signalised junctions;
2. reproduce Indian vehicle mix, lateral filtering/seepage and variable demand;
3. measure demand and queues in both vehicle counts and PCU;
4. attach different traffic-signal controllers through one common interface;
5. run the same scenario, seeds and metrics for a fair comparison;
6. inspect every assumption, input and calibration result.

### Success statement

> A new user can clone the repository, build the reference corridor, reproduce the field-informed traffic profile, run at least three signal controllers, and obtain the published metrics with one documented command.

---

## 2. What the simulator is—and is not

### It is

- a SUMO-based benchmark and scenario package;
- configurable rather than restricted to four junctions;
- designed around Indian mixed vehicle classes and weak lane discipline;
- calibrated against disclosed field observations;
- a common test bed for Saarathi and other controllers.

### It is not

- a new traffic-simulation engine replacing SUMO;
- the first Indian mixed-traffic simulator—SiMTraM already extended SUMO for heterogeneous, non-lane movement;
- a complete digital twin of Bengaluru;
- credible merely because bikes and autos were added to SUMO;
- a platform that can use one universal PCU value under every traffic condition.

---

## 3. Reference corridor research

### Candidate reference corridor

**HAL Old Airport Road, Bengaluru: Domlur Flyover to HAL Main Gate.**

Google Maps currently shows the direct corridor as approximately **2.8 km**. It is a useful candidate because it is an arterial with mixed vehicles, major access points, side-road interactions, buses, flyover/at-grade geometry and multiple potential signal nodes. This is a **candidate**, not a final network definition.

Map evidence inspected:

- [Domlur Flyover → HAL Main Gate corridor](https://www.google.com/maps/dir/Domlur+Flyover,+Bengaluru/HAL+Main+Gate,+Bengaluru)
- [Domlur Flyover satellite view](https://www.google.com/maps/@12.9605888,77.6417115,18z/data=!3m1!1e3)
- [HAL Main Gate satellite view](https://www.google.com/maps/@12.9585434,77.6661926,18z/data=!3m1!1e3)

### Important map limitation

Google Maps imagery is reconnaissance evidence, not sufficient engineering ground truth. Before building the final network, verify on site:

- which intersections are actually signalised;
- signal phase order and permitted turns;
- number and effective width of approaches;
- flyover versus at-grade movements;
- medians, service roads, bus stops, U-turns, free left turns and access roads;
- stop-line locations and queue storage;
- whether construction or temporary diversions are present.

### Corridor selection gate

Choose the corridor only if all are true:

- [ ] 3–6 consecutive signalised nodes are observable and modelable.
- [ ] Safe public observation points exist for traffic counts.
- [ ] The corridor has meaningful through traffic and side-road demand.
- [ ] Geometry can be reconstructed from OSM plus field verification.
- [ ] Signal phases/timings can be observed without accessing restricted infrastructure.
- [ ] No single grade separation makes the whole corridor unreasonably complex for the capstone.

If Domlur is too complex, choose a simpler Bengaluru arterial. The scientific method remains the same.

---

## 4. What the published research requires us to do

### 4.1 PCU is context-dependent

IRC 106:1990 explicitly states that PCU factors do not remain constant; they depend on vehicle dimensions/speeds and traffic composition. Its urban-road table changes factors depending on whether a vehicle class is about 5% or at least 10% of the stream. For example, the table gives two-wheelers as 0.5 or 0.75 and trucks/buses as 2.2 or 3.7 depending on composition.

Indian signalised-intersection studies go further:

- Padinjarapat and Mathew estimate saturation flow and PCUs together from field discharge data at six locations.
- Alex and Isaac show dynamic PCU sensitivity to approach width, composition, speed and flow.
- Patel and Dhamaniya report wide observed PCU ranges across vehicle classes and metropolitan intersections.
- Static IRC values remain useful as a transparent baseline, but they must not be presented as universal truth.

**Design decision:** support two modes:

1. `pcu_mode: static_irc`—published static factors, clearly cited;
2. `pcu_mode: calibrated`—corridor-specific factors derived from field data, with uncertainty/sensitivity reported.

Do not silently use one fixed dictionary for every experiment.

### 4.2 “Non-lane traffic” requires behavioural calibration

SUMO's sublane model supports multiple two-wheelers in parallel, virtual-lane formation, lateral position/speed and aggressive encroachment. Activating `--lateral-resolution` alone does not prove realism.

Field and simulation literature identifies behaviours that must be checked:

- lateral seepage/filtering toward the stop line;
- staggered queues and multiple leaders;
- class-specific dimensions, acceleration and minimum gaps;
- saturation discharge by approach width and vehicle composition;
- lateral clearance and lane-changing aggressiveness;
- queue spread across the full carriageway width.

**Design decision:** calibrate the simulator against both macroscopic and behavioural targets, not only total flow.

### 4.3 Validation must be separate from calibration

Parameters fitted to one observation period must be tested against a different time period or day. Report measures such as GEH for turning flows, RMSE/MAE for queues or travel time, and error in saturation discharge. Do not call the model validated using the same samples used to tune it.

### 4.4 The simulator contribution is reproducibility

SiMTraM and multiple Indian mixed-traffic models already exist. Saarathi becomes useful by releasing a current, runnable SUMO scenario, field inputs, controller API, experiment protocol and raw results together.

---

## 5. Target system architecture

```text
Field survey + published sources + OSM/Map reconnaissance
                         │
                         ▼
               Corridor manifest (YAML)
       geometry · nodes · signals · vehicle classes
       PCU modes · demand profiles · calibration bounds
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
  SUMO network builder          Demand/route builder
  OSM + verified edits          turning counts + time bins
          └──────────────┬──────────────┘
                         ▼
              Mixed-traffic SUMO model
        sublane + vehicle behaviour + signal plans
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Fixed-time      Actuated      Max-Pressure
                                          │
                                          ▼
                               Saarathi controller later
                         │
                         ▼
             Common experiment and metrics layer
       seeds · tripinfo · queues · PCU · discharge · CSV
                         │
                         ▼
              Calibration/validation report + release
```

### Required configuration structure

```text
scenarios/<corridor>/
├── corridor.yaml              # authoritative scenario manifest
├── source.osm                 # frozen OSM extract, with date/source
├── network/                   # generated and verified SUMO network
├── signals/                   # observed/assumed phase plans
├── demand/                    # raw counts, cleaned counts, route flows
├── calibration/               # bounds, runs, selected parameters
├── validation/                # held-out observations and scores
└── README.md                  # assumptions and reproduce commands
```

The code must derive the node count from the manifest. `N_JUNCTIONS = 4` must not appear independently in the network builder and demand generator.

---

## 6. Data collection plan

### Observation periods

Collect at least:

- weekday AM peak: 60 minutes;
- weekday midday/off-peak: 45–60 minutes;
- weekday PM peak: 60 minutes;
- one additional held-out period for validation.

Use 5- or 15-minute bins. Preserve raw counts before aggregation.

### Record at every selected signal

- approach and turning-movement counts;
- classified counts: two-wheeler, auto-rickshaw, car/jeep/van, LCV, bus, truck;
- red/yellow/green start and end times by phase;
- maximum and average queue by approach;
- queue-clearance time and saturated-green discharge;
- observed spillback/blocking;
- buses stopping near the junction;
- free-left/U-turn/pedestrian interference as notes;
- weather, incident and construction notes.

### Safety and privacy

- Observe only from safe public locations.
- Do not record faces or licence plates as research variables.
- Store counts/trajectories, not personal identities.
- If institutional permission is required for video collection, obtain it before recording.

---

## 7. Vehicle and PCU model

### Minimum vehicle classes

| Class | Required SUMO properties | PCU treatment |
|---|---|---|
| Two-wheeler | measured width/length, high lateral flexibility, small lateral gap | static IRC baseline + calibrated sensitivity |
| Auto-rickshaw | separate dimensions and behaviour; never model as a generic car without justification | static baseline + calibrated sensitivity |
| Car/jeep/van | reference class | 1.0 reference |
| LCV | distinct from car and heavy truck | separate factor |
| Bus | long vehicle, low acceleration, bus-stop effects where present | separate factor |
| Truck | heavy/long vehicle; separate from bus when sample allows | separate factor |

### PCU implementation rule

PCU belongs in a named sensing/analysis layer. Keep raw classified vehicle counts alongside every PCU aggregate so results can be recomputed using alternative factors.

Required outputs per approach and interval:

- raw count by class;
- static-IRC PCU total;
- calibrated-PCU total;
- stopped PCU and moving PCU;
- factor set and version used.

---

## 8. Calibration and validation plan

### Calibration parameters

- vehicle dimensions and maximum speeds;
- acceleration/deceleration and driver imperfection;
- longitudinal `minGap`;
- `minGapLat`, `lcSublane`, `lcPushy`, lateral alignment;
- route/turn proportions;
- arrival distribution and peak-hour factors;
- bus-stop dwell and blockage if applicable.

### Calibration targets

1. turning movement volume by time bin;
2. journey time across the corridor;
3. approach queue length and clearance time;
4. saturation discharge by approach;
5. vehicle-class share;
6. qualitative/quantitative lateral queue occupancy.

### Acceptance gates

The project must set thresholds before tuning. Recommended starting gates:

- at least 85% of turning-flow observations with GEH < 5;
- corridor travel-time error ≤ 15% in calibration and validation periods;
- median approach queue error ≤ 20%;
- modal-share error ≤ 5 percentage points for major classes;
- no systematic collision/teleportation dependence;
- visible two-wheeler filtering and staggered queueing consistent with field evidence.

These are project acceptance criteria, not universal standards. If a gate is infeasible, document the failure and revise it before evaluating controllers—not after seeing controller results.

---

## 9. Controller-neutral benchmark protocol

Every controller must receive:

- the same network and routes;
- the same seed set;
- the same warm-up and evaluation windows;
- equivalent safety constraints;
- observations with a declared sensing assumption;
- the same metric calculation.

### Minimum controllers for simulator release

1. SUMO fixed-time plan;
2. SUMO actuated control;
3. tuned PCU-aware Max-Pressure;
4. vehicle-count Max-Pressure as a PCU ablation.

Saarathi PPO and neighbour messaging belong after these four are stable.

### Required metrics

- completed trips and throughput;
- travel time and time loss;
- waiting time and stops per vehicle;
- queue length/PCU and spillback;
- per-class delay;
- corridor journey time;
- collision, emergency-braking and teleport counts;
- runtime and seed-level raw results.

---

## 10. Current-code gap analysis

| Current implementation | Problem | Required correction |
|---|---|---|
| Synthetic equally spaced corridor | Does not reproduce a real signal layout | Create manifest-driven OSM/field-verified reference scenario; retain synthetic scenario only for unit tests |
| Earlier `N_JUNCTIONS = 4` constants | Network size was duplicated and locked | **Resolved in the prototype:** network builder, demand generator and runner now read `corridor.yaml`; the PPO observation adapter still targets the reference 4-arm signal layout |
| Fixed vehicle mix and hourly profile | No field basis | Generate demand from classified turning counts and documented time bins |
| Fixed `PCU` dictionary | Ignores context dependence | Add versioned static and calibrated PCU modes; always retain raw class counts |
| Sublane resolution = 0.4 m | Feature enabled but not calibrated | Tune lateral and longitudinal parameters against field evidence |
| Auto-generated signal phases | May not match real movements/intergreens | Encode verified signal phase plans and permitted turns |
| `collision.action="warn"` and 600 s teleport | Can hide invalid behaviour | Report collisions/teleports and reject parameter sets dependent on them |
| Basic tripinfo metrics | No queue, discharge, per-class or calibration scores | Add detector/TraCI time-series metrics and validation reports |
| README refers to missing assumptions file | Assumptions not auditable | Create and maintain `docs/assumptions.md` |

---

## 11. Work plan with checklist

### Phase 0 — freeze the research question

**Goal:** define the simulator contribution before coding.

- [ ] Approve the main research question.
- [ ] Confirm the reference corridor selection criteria.
- [ ] Freeze vehicle classes and minimum metrics.
- [ ] Separate simulator scope from Saarathi-controller scope.
- [ ] Create the assumptions register.

**Exit gate:** one-page signed scope; no “first simulator” claim.

### Phase 1 — corridor reconnaissance and field sheet

**Goal:** produce a verified node/movement inventory.

- [ ] Inspect corridor and junctions using Google Maps/OSM.
- [ ] Visit the corridor and verify signalised nodes.
- [ ] Draw every permitted movement and phase.
- [ ] Record widths, lane use, medians, bus stops, U-turns and free lefts.
- [ ] Choose safe counting locations and survey periods.
- [ ] Prepare count sheets and time-synchronisation method.

**Exit gate:** corridor inventory, map, photos/notes and survey plan reviewed by the guide.

### Phase 2 — field data collection

**Goal:** obtain calibration and held-out validation evidence.

- [ ] Collect classified turning counts.
- [ ] Record signal timing and queues.
- [ ] Extract/clean time-binned data.
- [ ] Split calibration and validation periods before tuning.
- [ ] Document anomalies and missing observations.

**Exit gate:** raw and cleaned data committed with a data dictionary.

### Phase 3 — configurable scenario builder

**Goal:** eliminate hard-coded four-junction assumptions.

- [ ] Define `corridor.yaml` schema.
- [ ] Import/freeze OSM geometry.
- [ ] Apply documented network edits.
- [ ] Encode signal plans and intergreens.
- [ ] Generate routes from turning counts.
- [ ] Make any node count work from the manifest.
- [ ] Add schema/network unit tests.

**Exit gate:** one command rebuilds the same network and demand files.

### Phase 4 — mixed-traffic behaviour and PCU

**Goal:** reproduce measurable Indian mixed-traffic characteristics.

- [ ] Implement all vehicle classes.
- [ ] Add static-IRC and calibrated PCU factor sets.
- [ ] Retain raw class counts in every metric file.
- [ ] Tune sublane/driver parameters within declared bounds.
- [ ] Check filtering, staggered queues and discharge visually.
- [ ] Report collision and teleport counts.

**Exit gate:** parameters satisfy behavioural and safety sanity checks.

### Phase 5 — calibration and independent validation

**Goal:** show that simulated traffic resembles held-out observations.

- [ ] Run automated calibration search.
- [ ] Freeze the chosen parameter set.
- [ ] Evaluate on held-out periods without retuning.
- [ ] Produce GEH, travel-time, queue, discharge and modal-share tables.
- [ ] Explain every missed target.

**Exit gate:** validation report passes predeclared thresholds or transparently documents limitations.

### Phase 6 — benchmark controllers

**Goal:** prove the environment is useful for fair comparison.

- [ ] Fixed-time baseline.
- [ ] Actuated baseline.
- [ ] Vehicle-count Max-Pressure.
- [ ] PCU-aware Max-Pressure.
- [ ] At least 5 seeds per scenario.
- [ ] Mean, standard deviation/95% CI and raw results.
- [ ] Lane-disciplined versus mixed/sub-lane sensitivity experiment.

**Exit gate:** one reproducible baseline table and two ablation figures.

### Phase 7 — open release and paper package

**Goal:** make the simulator independently usable.

- [ ] Installation and one-command reproduction guide.
- [ ] Scenario manifest, source dates and licences.
- [ ] Raw/cleaned anonymised counts and data dictionary.
- [ ] Calibration and validation scripts/results.
- [ ] Controller API and baseline implementations.
- [ ] Seeds, environment lock file and hardware/runtime notes.
- [ ] Archive a tagged release with a persistent identifier if possible.

**Exit gate:** a new team member reproduces the headline table without private instructions.

---

## 12. Team task split

| Owner | Main responsibility | Weekly evidence |
|---|---|---|
| Simulation/geometry lead | corridor manifest, OSM edits, signal plans, network QA | rebuilt network + geometry change log |
| Data/calibration lead | field sheets, counts, PCU estimation, calibration/validation | cleaned dataset + validation dashboard/table |
| Software/experiments lead | scenario API, controllers, metrics, seeds, release automation | reproducible run + raw result bundle |

All three members participate in at least one field observation and review each other's assumptions.

---

## 13. Paper-ready outputs

The simulator phase is complete only when these artefacts exist:

1. corridor map and node/movement table;
2. raw and cleaned classified turning counts;
3. vehicle-class and PCU factor table with sources;
4. calibrated SUMO parameter table;
5. calibration-versus-validation results;
6. fixed, actuated and Max-Pressure baseline table across seeds;
7. PCU versus vehicle-count ablation;
8. lane-disciplined versus sublane/mixed-traffic ablation;
9. repository release and reproduction instructions;
10. limitations section covering one corridor, simulator assumptions and transferability.

---

## 14. Key published sources

- IIT Bombay, **SiMTraM—Simulation of Mixed Traffic Mobility**: [project page](https://www.civil.iitb.ac.in/tvm/SiMTraM_Web/html/).
- IRC 106:1990, **Guidelines for Capacity of Urban Roads in Plain Areas**: [document](https://law.resource.org/pub/in/bis/irc/irc.gov.in.106.1990.pdf).
- Padinjarapat & Mathew (2021), **Estimation of saturation flow for non-lane based mixed traffic streams**: [DOI](https://doi.org/10.1080/21680566.2020.1781708).
- Alex & Isaac (2015), **Dynamic PCU Values at Signalised Intersections in India for Mixed Traffic**: [DOI](https://doi.org/10.7708/ijtte.2015.5(2).09).
- Patel & Dhamaniya (2021), **Developing Mixed Traffic Equivalency Factors to Estimate Saturation Flow at Urban Signalized Intersections**: [DOI](https://doi.org/10.1177/03611981211018694).
- Singh & Rao (2023), **Simulation of Signalized Intersection with Non-Lane-Based Heterogeneous Traffic Conditions Using Cellular Automata**: [DOI](https://doi.org/10.1177/03611981231211317).
- Agarwal et al. (2024), **Dynamic traffic signal control for heterogeneous traffic conditions using Max Pressure and Reinforcement Learning**: [DOI](https://doi.org/10.1016/j.eswa.2024.124416).
- SUMO, **Sublane Model documentation**: [official documentation](https://sumo.dlr.de/docs/Simulation/SublaneModel.html).
- Lopez et al. (2018), **Microscopic Traffic Simulation using SUMO**: [DOI](https://doi.org/10.1109/ITSC.2018.8569938).

---

## 15. Immediate next sprint

Do these tasks before further PPO or neighbour-message development:

- [ ] Create `corridor.yaml` schema and remove duplicated junction-count constants.
- [ ] Create `docs/assumptions.md` with source, value, uncertainty and validation status for every assumption.
- [ ] Create the classified turning-count survey sheet.
- [ ] Conduct a field reconnaissance of the candidate corridor.
- [ ] Decide calibration and validation observation periods.
- [ ] Implement actuated and vehicle-count Max-Pressure baselines.
- [ ] Add collision, teleport, queue, discharge and per-class metrics.

**Main rule:** no controller-performance claim is paper-ready until the simulator passes independent validation.
