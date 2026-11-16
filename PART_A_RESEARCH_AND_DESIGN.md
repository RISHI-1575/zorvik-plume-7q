# Part A — Indian Road Simulation: Research and Design

**Date:** 2026-11-10 · **Scope:** Part A only (the environment). The node-based controller (Part B) is out of scope here.
**Bound by:** `RULES.md`. Nothing here overrides its claim, calibration or fairness rules.

---

## 0. Short answer

**We already are on SUMO.** `code/` runs real SUMO 1.27.1 through TraCI: the sublane model, six Indian vehicle classes and a manifest-driven corridor. The thing that looked like "our own website" is `showcase/dashboard.html`. It is a JavaScript mock for presentations and has no simulator behind it. It is not Part A.

The best Part A is **not a new simulator and not a fork of SUMO**. It is an **open, calibrated "Indian scenario pack + plug-in harness" on top of stock SUMO**, made of four parts:

1. A real Bengaluru corridor built from OpenStreetMap: HAL Old Airport Road, Domlur → Marathahalli.
2. A versioned Indian vehicle-behaviour library tuned to published two-wheeler seepage evidence.
3. Demand and signal timings from real sources: field counts and the public Bengaluru Traffic Police (BTP) signal-timing PDFs.
4. A plug-in API so anyone can run their own controller in three ways: as a Python class, through Gymnasium or PettingZoo, or through raw TraCI. All three use the same scoring harness.

This matches what the literature shows is missing (§3). It also avoids the mistake that killed SiMTraM (§2).

---

## 1. How SUMO works, in five layers

| Layer | What it is | SUMO tool | Our file |
|---|---|---|---|
| **Network** | Roads as *edges* split into lanes, *junctions* with connections and traffic-light programs | `netconvert` (from OSM or our node/edge XML), `netedit` (visual editor) | `corridor.net.xml` |
| **Vehicle types** | Size, acceleration, gaps and lane-change behaviour per class | `vType` in an additional file | `vtypes.add.xml` |
| **Demand** | Who drives where and when: flows, routes, trips | `routeSampler.py` (counts → routes), `duarouter` | `routes.rou.xml` |
| **Simulation** | Step-by-step microsimulation. The **sublane model** (`--lateral-resolution 0.4`) splits each lane into 0.4 m strips, so bikes can squeeze beside cars | `sumo` (headless), `sumo-gui` (visual) | `corridor.sumocfg` |
| **Control and output** | Python drives the simulation live through **TraCI** (read queues, set signal phases). Outputs include trip info, trajectories (FCD) and detectors | `traci`, `sumolib` | `src/saarathi/*` |

A controller is a Python loop. It calls `traci.simulationStep()`, reads the state, then calls `traci.trafficlight.setPhase(...)`. Any algorithm in any library can sit in that loop. This is why SUMO already *is* the "platform people can run their own algorithms on". Our job is to give them an Indian scenario worth running on.

**Screenshots:** these are real renders of our corridor, made headlessly through TraCI with `code/render_sumo.py`:
- `docs/sumo_screens/j2_closeup.gif`: two-wheelers filter laterally between queued trucks and cars at junction J2.
- `docs/sumo_screens/zoom_0420.png`, `docs/sumo_screens/overview_t600.png`: the corridor at peak.
- Run used for these renders: seed 42, 1,122 vehicles inserted in 900 s, mean speed 7.39 m/s.

**Running the live GUI on macOS:** the pip SUMO's `sumo-gui` and `netedit` need X11. Install XQuartz with `brew install --cask xquartz`, log out and back in, then run `sumo-gui -c code/scenarios/corridor4/corridor.sumocfg`.

---

## 2. What already exists (landscape)

| Work | What it is | Status | Lesson for us |
|---|---|---|---|
| **SiMTraM** (IIT Bombay, T. V. Mathew) | GPL *fork* of an old SUMO, adding heterogeneous non-lane traffic and gradual lane change | v0.1.0 on SourceForge, **1 June 2012**, no later release | Forking a simulator dies with the fork. SUMO later shipped its own sublane model and left the fork behind. **Do not fork.** |
| "Comparison of SUMO and SiMTraM for Indian Traffic" (Transp. Res. Procedia) | Head-to-head comparison | Published | Even stock SUMO can represent Indian traffic if parameters are calibrated |
| **HETEROSIM** (IIT Madras, Arasan & Koshy 2005) | C++ heterogeneous-traffic microsimulator, used in many IITM papers | Research code, not publicly distributed | Strong behaviour models, zero reuse by others. Openness is the gap. |
| VISSIM / Aimsun calibrations (Mathew & Radhakrishnan; Maheshwary et al.) | Calibration of commercial tools for Indian signalised junctions | Published, commercial software | They give the **calibration method** we copy: class-specific parameters plus field counts |
| **Two-wheeler seepage in SUMO** (Computer Networks 287, 112510, 2026) | Calibrated SUMO to 310,110 Indian video frames | Published | Mean seepage gap **0.906 m**, against the usual ~2.5 m minimum gap. The calibrated run had **80,553 seepage events vs 132** with defaults. This is the best evidence for our bike profile. |
| SUMO calibrations for Egypt (MDPI Sustainability 18(14):7025, 2026) and Khulna, Bangladesh (Chowdhury & Chakraborty 2024) | Genetic-algorithm and sensitivity calibration for heterogeneous roads | Published | **Calibration method matters more than car-following model choice** (MAPE: IDM 8.8%, W99 8.9%, Krauss 10.6%). The key parameters are `lcSpeedGain`, `lcStrategic` and `lcOpposite`. |
| RESCO (NeurIPS 2021), sumo-rl, LibSignal, CityFlow | RL traffic-signal benchmarks and environments | Maintained, widely cited | Their scenarios are all **Western or Chinese, lane-disciplined**. sumo-rl's Gymnasium/PettingZoo API is the de-facto standard, so we should be compatible with it. |
| Indian SUMO projects on GitHub (e.g. Bengaluru ISA project, PyCon India 2019 talk) | One-off student or research scenarios | Uncalibrated, undocumented | Many exist, so "first" claims are false. None are a reusable, calibrated benchmark. |

**Data sources found:**

| Source | What it gives | Use |
|---|---|---|
| **BTP signal timings on OpenCity** (`data.opencity.in/dataset/bengaluru-city-traffic-signal-data`, updated 27 Nov 2025) | PDFs for ~200 Bengaluru junctions, including **Domlur Water Tank, Marathahalli Bridge & Yamlur, ISRO / Kadubeesanahalli**, on or next to our corridor | Real fixed-time plans for the baseline. The fields inside the PDFs and the licence still need checking. |
| **UVH-26** (IISc AIM; HuggingFace `iisc-aim/UVH-26`, arXiv 2511.02563) | 26,646 Bengaluru CCTV frames, 1.8 M boxes, 14 Indian vehicle classes | Modal-split prior, and a detector for counting our own videos |
| Kanagaraj et al. 2015 (TRR 2491), Chennai trajectories | Mixed-traffic vehicle trajectories | Validating lateral gaps and speeds per class |
| Indo-HCM 2017 (CSIR-CRRI) | PCU and saturation flow from 18 Indian signalised intersections | Checking saturation flow and discharge rate, plus the PCU sensitivity set |
| IRC 106:1990 | Composition-dependent PCU | The `static_irc` baseline set (already in the manifest) |
| OSM via `osmGet.py` / `osmWebWizard.py` (bundled in our `.venv`) | Road geometry | Network build |

---

## 3. The gap we fill

There is **no maintained, open, calibrated SUMO benchmark for Indian mixed, weak-lane-discipline traffic** that also ships a plug-in controller API and a fixed scoring protocol. The pieces exist separately:
- the behaviour evidence (the seepage paper);
- calibration methods (the Egypt and Bangladesh papers, the VISSIM India papers);
- real signal data (BTP / OpenCity);
- RL APIs (sumo-rl).

Nobody has assembled them. That assembly, and the honesty labels on every number, is Part A's contribution. It is the safe claim already in `RULES.md` §2.

---

## 4. The design

### 4.1 Principles
1. **Stock SUMO only.** Every customisation goes through SUMO's own files and parameters. Upgrading SUMO must never break us.
2. **The manifest (`corridor.yaml`) stays the single source of truth.** Every layer below is generated from it.
3. **Every parameter carries a status label:** `provisional → sourced → measured → calibrated → validated` (as in `docs/assumptions.md`).
4. **Same harness for everyone.** A user's algorithm is scored by exactly the same code, seeds and metrics as our baselines.

### 4.2 Layers

**L1 — Network: real corridor from OSM.**
- Steps: `osmGet.py` downloads the bounding box → `netconvert --osm` with an Indian type map → manual fixes in `netedit` (medians, U-turn gaps, free left turns, bus bays) → `network/corridor.net.xml`.
- Indian roads often have no usable lane markings. We model each carriageway at its **measured width** and let the sublane model decide the lateral positions, instead of trusting the painted lane count.
- Keep the synthetic `corridor4` as the fast test scenario.
- Manifest knob: `network.source: osm | synthetic`.

**L2 — Vehicle behaviour library.**
- Each class (bike, auto, car, lcv, bus, truck) gets a parameter set: size, accel/decel, `minGap`, `minGapLat`, `latAlignment`, `lcSublane`, `lcPushy`, `lcSpeedGain`, `lcStrategic`, `sigma`.
- Ship **three named profiles**, each selected in the manifest (`behaviour.profile`):
  - `lane_disciplined`: SUMO defaults. This is the ablation baseline.
  - `literature`: starting values from the seepage paper and the Egypt/Bangladesh calibrations, each row cited.
  - `calibrated`: the output of L5.
- The profile switch *is* the paper's "lane-disciplined vs sublane" ablation (`RULES.md` §5.6).

**L3 — Demand from counts.**
- Classified turning counts per approach per 15 minutes go into the manifest (or a CSV next to it). SUMO's bundled **`routeSampler.py`** turns them into routes, so we need no custom route maths.
- If we have no local counts yet, use the UVH-26 modal share as a labelled `sourced` prior.
- Time profiles: AM peak, midday and PM peak, with one held-out period.

**L4 — Signals from BTP data.**
- Read cycle length and phase splits from the OpenCity BTP PDFs for the corridor junctions, then write them as SUMO `tlLogic` programs.
- The result is "fixed-time" meaning **today's real Bengaluru timing**, not a guessed 30 s cycle. The baseline becomes much stronger and much more honest.
- Safety timings (min green, yellow, all-red) move from `config.py` constants into the manifest, as `RULES.md` §6.1 already requires.

**L5 — Calibration and validation.**
- Search over the L2 parameters to minimise GEH on the tuning counts, then check on the **held-out** period. The search starts as a simple random or genetic search using what is already installed, and no new dependency is added until it is too slow.
- The acceptance gates are the ones already in `RULES.md` §4.3: GEH < 5 on ≥85% of flows, travel time ±15%, queue ±20%, modal share ±5 pp, zero reliance on collisions or teleports.

**L6 — Realism checks.** These are behavioural tests, not settings. Each one prints PASS or FAIL:
- two-wheeler seepage count to the stop line;
- share of bikes in the front row at red;
- staggered queue shape;
- discharge headway and saturation flow against Indo-HCM;
- lateral-gap distribution against the Kanagaraj trajectories.

`RULES.md` §3.4 says the sublane model is not evidence of realism; these checks are the evidence.

**L7 — The plug-in harness ("bring your own algorithm").** Three ways in, one scorer:

| Entry point | Who it is for | How |
|---|---|---|
| **Python class** | Rule-based or optimisation researchers | Any class with `__init__(tls_id)` and `step(t, dt)` that requests phases through our `SafetyShell`. Run with `python run.py --controller mypkg.module:MyController`. |
| **Gymnasium / PettingZoo** | RL researchers | The scenario's `net.xml` and `rou.xml` load directly into **sumo-rl**'s `SumoEnvironment`, so the existing RESCO/sumo-rl code runs on Indian traffic with zero changes. We also keep our own PCU-observation env (`env.py`). |
| **Raw TraCI** | Anyone else: C++, Java, MATLAB, external software | Start `sumo -c corridor.sumocfg --remote-port N` and connect any TraCI client, then score the run's `tripinfo.xml` with `summarize_results.py`. |

Every route ends in the **same metric code**: delay, travel time, waiting, stops, queue, per-class delay, collisions and teleports. The per-class delay shows whether a controller helps cars at the cost of bikes and buses.

**L8 — Scenario knobs (what users customise without code).** All of these live in `corridor.yaml`:

| Knob | Values |
|---|---|
| Corridor | `corridor4` (synthetic) · `old_airport_road` (OSM) · any new folder built from OSM |
| Time window | AM / midday / PM / held-out |
| Demand scale | e.g. 0.8–1.3× |
| Modal split | per-class shares |
| Behaviour profile | `lane_disciplined` · `literature` · `calibrated` |
| PCU set | `static_irc` · `indo_hcm` · `calibrated` |
| Signal plan | `btp_fixed` · `actuated` · external controller |
| Events | ambulance run (later, Part B), lane blockage or bus-stop dwell |

**L9 — Packaging and visuals.**
- `python verify.py` rebuilds everything and runs the contract tests plus the L6 checks.
- `python run.py --compare` produces the leaderboard table.
- `sumo-gui` gives the live view and `render_sumo.py` gives headless GIFs.
- A versioned release archive ships with data licences, as in `RULES.md` §7.4.

### 4.3 What we deliberately do **not** build
- **No custom simulator or web simulator.** SUMO's car-following, sublane and TraCI are decades of validated work. A JavaScript re-implementation would be less realistic and nobody else could reuse it.
- **No SUMO fork.** SiMTraM shows how that ends.
- **No CARLA, MetaDrive or 3D.** They are for vehicle perception and driving policy, are compute-heavy, and are the wrong scale for signal control.
- **No city-scale scenario yet.** One calibrated corridor is worth more than an uncalibrated city.

---

## 5. Gaps in today's code that block "bring your own algorithm"
Status after the A1–A4 build (2026-11-10):
1. **Controllers were hard-coded.** Fixed: `--controller module:Class` or `file.py:Class` (`controllers.load_controller`); template in `code/examples/my_controller.py`.
2. **Scenario selection.** The `SAARATHI_SCENARIO` env var already existed; `run.py --scenario <corridor.yaml>` now sets it.
3. ~~Safety timings are code constants~~: wrong in the first draft. They were already read from the manifest `safety:` block.
4. **Raw-TraCI / sumo-rl path.** Every scenario writes a plain `corridor.sumocfg`, so sumo-rl and raw TraCI can load it directly. Not yet tested with sumo-rl.
5. **Realism checks.** First check added: `front_row_bike_share` (two-wheeler share of vehicles halted within 8 m of a red stop line) next to the bike modal share. The other L6 checks are still to do.

---

## 6. Milestones (riskiest first; each has a pass/fail check)

| # | Milestone | Done when |
|---|---|---|
| A1 | **Real corridor from OSM:** Old Airport Road, Domlur → Marathahalli, through `osmGet` + `netconvert` + `netedit` fixes | It runs 1 h of demand with 0 teleports (current: ~1.3% at unsignalled side-road junctions, reported). Junction count and approach widths match satellite imagery. |
| A2 | **BTP signal plans:** download the corridor PDFs, check licence and fields, convert to `tlLogic` | The `btp_fixed` plan runs, and its cycle and splits match the PDF |
| A3 | **Behaviour profiles + realism checks (L2, L6)** | `literature` shows clearly more seepage than `lane_disciplined`; check output is archived |
| A4 | **Plug-in harness (L7):** external class loader, `--scenario`, manifest safety timings, sumo-rl load test | A 10-line example controller in a separate file runs and is scored. sumo-rl's `SumoEnvironment` steps the corridor. |
| A5 | **Field counts + calibration (L3, L5):** 2–3 junctions, AM / mid / PM, one period held out | The `RULES.md` §4.3 gates are reported against held-out data, whether they pass or fail |
| A6 | **Release:** docs, licences, seeds, environment lock, tagged archive | A fresh clone reproduces the leaderboard with one command |

A1–A4 need no field work and can start now. A5 is the only part that needs the team on the road, and it is the part that makes the work publishable.

---

## 7. Sources
- SiMTraM project page (SourceForge), release v0.1.0, 2012-06-01.
- "Comparison of SUMO and SiMTraM for Indian Traffic Scenario Representation", *Transportation Research Procedia* (ScienceDirect S2352146516306962).
- Arasan & Koshy (2005), HETEROSIM; follow-up papers in ECMS 2010, *Transport* 2010, ASCE JTE.
- Mathew & Radhakrishnan, "Calibration of Microsimulation Models for Nonlane-Based Heterogeneous Traffic at Signalized Intersections".
- Maheshwary et al., vehicle-class-specific VISSIM calibration methodology.
- "Modeling and benchmarking two-wheeler seepage behavior in dense mixed traffic simulations", *Computer Networks* 287 (2026) 112510, doi:10.1016/j.comnet.2026.112510.
- Shahdah et al., SUMO calibration for Egyptian heterogeneous two-lane roads, *Sustainability* 18(14):7025 (2026); Chowdhury & Chakraborty (2024), Khulna; Chaudhari et al. (2022), TRR; Harth et al. (2022); Kappenberger (2025).
- Kanagaraj et al. (2015), TRR 2491, Chennai mixed-traffic trajectory data.
- UVH-26, IISc AIM, arXiv 2511.02563, HuggingFace `iisc-aim/UVH-26`.
- Indo-HCM (2017), CSIR-CRRI; IRC 106:1990.
- Bengaluru City Traffic Signal Data, OpenCity (BTP), updated 2025-11-27.
- Ault & Sharon (2021), RESCO, NeurIPS Datasets & Benchmarks; sumo-rl (LucasAlegre, v1.4.5); LibSignal; CityFlow.
- SUMO docs: Import from OpenStreetMap, Sublane model, routeSampler, TraCI.

Paper venues above were checked on the publisher page during this research, except where a preprint is named. Before citing any of them in the paper, confirm each against `RULES.md` §2's citation rule.
