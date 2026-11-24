# Saarathi — Deep Gap Review (Part A + Part B together)

Date: 2026-11-24. Scope: published, peer-reviewed work first; preprints are included only where they are the main threat or the only evidence, and are labelled **[PP]**. **[P]** = published (journal/conference, DOI or venue given).

This file adds to `PART_A_LIT_GAP_REVIEW.md` (gaps G1–G6) and `LITERATURE_AUDIT.md`. It does not replace them, and it changes no scope. The authority order still holds: PROJECT_DEFINITION → FINAL_PLAN → RULES.

## 0. Honest coverage statement

I did **not** read every word of every paper. Here is what I actually read:

- **Full text:** the 22 local PDFs in the project scratch set. Many of them are generic MARL papers with little relevance.
- **Abstract plus conclusion/limitations only:** everything else listed below. The text came from the research index.
- **Not read:** paywalled full texts (for example, TR-C versions). Where only an arXiv version was readable, I note it.

Every claim in sections 2–3 traces to a source in section 1. Anything beyond that is labelled *inference*.

---

## 1. Sources, grouped

### 1a. Indian / heterogeneous / laneless traffic (Part A core)

| Source | Status | What it does | Limitation that matters for Saarathi |
|---|---|---|---|
| Nandakumar, Banerjee & Vanajakshi — laneless RL-TSC, arXiv:2509.21745 (v. 2026-11-03) | **[PP]** | Single non-orthogonal laneless junction in Chennai, built in SUMO. Queue reward at approach level. Reports 66–73% lower queue than Dynamic Webster, and beats actuated control and RESCO-DQN. Releases an "open" laneless SUMO framework. | Covers one junction only and reports queue only. Has **no max-pressure baseline** and no multi-junction or zero-shot test. Its repo (RLTSCQ) has **no licence**. **Main threat to any "first open Indian SUMO" wording.** |
| Chaudhuri et al. 2022, Springer SIST (arXiv 2109.00937) | **[P]** | RL TSC on a "Bengaluru" junction geometry. | Single-lane cars and synthetic Weibull demand. Queue metric only. No seeds reported and no max-pressure baseline. Bengaluru in name only. |
| Mattungal & Vanajakshi 2025, PLOS ONE, doi:10.1371/journal.pone.0319325 | **[P]** | Analytical delay model for multi-class lane-free (MCLF) traffic, using PCE and virtual lanes. Validated in VISSIM. | Not a controller study. **Use it as the delay-metric reference** for Indian MCLF traffic. |
| Sugiarto et al. 2021, PLOS ONE, doi:10.1371/journal.pone.0256620 | **[P]** | Bayesian PCE estimation. Motorcycle PCE is about 0.24 (Banda Aceh). | PCEs depend on the site. Manual code-book PCEs bias capacity estimates. |
| Sugiarto et al. 2024, PLOS ONE, doi:10.1371/journal.pone.0306112 | **[P]** | Base saturation flow for non-lane-based traffic. | Same point: saturation flow and PCU values depend on the context. |
| Sugiarto et al. 2025, MethodsX, doi:10.1016/j.mex.2025.103507 | **[P]** | Bayesian MCMC method for base saturation flow rate. | Gives a method to *propagate* PCU uncertainty, which nobody in TSC does. |
| Sadat et al. 2024, Environ. Health Insights, doi:10.1177/11786302241231706 | **[P]** | Lucknow SUMO model calibrated with field counts (emissions focus). | One of the very few published Indian SUMO calibrations. No signal-control comparison. |
| Lopez et al. 2018, IEEE ITSC (SUMO) | **[P]** | SUMO reference paper. It includes the sublane model (SL2015). | Sublane is **not validated for reduced lane discipline**. Opposite-lane overtaking is not compatible with sublane. |
| Kulkarni, Chaudhari, Srinivasan, Chilukuri, Treiber, Okhrin 2024, arXiv 2405.10665 | **[PP]** | Leader-follower identification and car-following calibration for non-lane Chennai traffic (Wiedemann-99). | Shows that laneless car-following calibration is still open. Done in VISSIM-style models, not SUMO sublane. |
| Eldhose, Chilukuri, Rajendran 2025, arXiv 2511.09946 | **[PP]** | Leader-follower identification under weak lane discipline. | Pairs that involve two-wheelers or heavy vehicles show the most variability. |
| Anagnostopoulos & Geroliminis 2022 | **[PP]** | Hybrid lane-based/lane-free model for motorcycles (pNEUMA, Athens). | Lane discipline depends on the vehicle mode, so one global sublane setting is a simplification. |
| Shirazi 2022, Sensors, doi:10.3390/s22197111 | **[P]** | Imports turning-movement counts into SUMO. | Tooling reference for the field-count pipeline. |
| Payra et al. 2026 "SIGMA", arXiv 2608.18263 | **[PP]** | Four intersections modelled on Kolkata, in SUMO. LLM-generated priority vectors for emergency vehicles. Bootstrap statistics. | A new Indian neighbour. Only a handful of junctions, lane-based, no field calibration. |
| Mundane, Manoharan, Singh 2026 (momentum reward) | **[PP]** | Indian authors. Compares a new reward against max-pressure. | Lane-based synthetic networks. |

### 1b. Evaluation rigour and benchmarks (Part A method)

| Source | Status | Key point |
|---|---|---|
| Agarwal et al. 2021 "Statistical Precipice", NeurIPS | **[P]** | Few-run RL results are unreliable. Report interval estimates, IQM and performance profiles. |
| Jayawardana et al. 2022 (task underspecification) | **[PP]** | Testing on a *family* of MDPs changes method rankings, with TSC as an example. Supports G2, G4 and G6. |
| Riehl, Kouvelas, Makridis 2026 "sumoITScontrol", arXiv 2604.23240 | **[PP]** | Many TSC studies rely on single runs, and the paper calls for variance-aware reporting and hypothesis tests. Ships max-pressure plus SCOOT- and SCATS-like controllers for SUMO. **Direct neighbour to Part A.** |
| Varela et al. 2021 | **[PP]** | Proposed standard methodology for RL-TSC evaluation. |
| Colas et al. 2019 | **[PP]** | Statistical tests for comparing RL algorithms. |
| LibSignal (published in *Machine Learning*; arXiv 2211.10649) | **[P]** | Cross-simulator TSC library with calibration across simulators. Lane-based. |
| Rafi et al. 2026 "Sim2Signal", arXiv 2609.01676 | **[PP]** | Splits the sim-to-real gap into observation, action, transition and reward parts, over 10 calibrated networks. How well a mitigation works depends on the network. **Major neighbour for a sensing/robustness gap.** |
| Nguyen et al. 2025 "T-REX" | **[PP]** | SUMO incident-robustness benchmark. Pressure-based methods degrade under incidents. |
| Su & Deng 2026 "LightSim" | **[PP]** | Cell-transmission simulator that preserves SUMO controller *rankings*. Ranking stability is now treated as a research object in its own right. |
| Shi et al. 2023 | **[PP]** | Missing sensor data and zero-shot transfer in TSC. |
| CoLight, CIKM 2019 | **[P]** | Graph-attention MARL. State uses lane counts and assumes homogeneous vehicles. |

### 1c. Controller, safety and emergency vehicles (Part B)

| Source | Status | Key point | Limitation that matters |
|---|---|---|---|
| Zhu & Tan 2026 "Com-MP", arXiv 2610.31037 | **[PP]** | RL learns a composition of max-pressure variants. Proves queue stability, stays robust under degraded sensing, transfers to unseen networks. | **Nearest prior art for the Part B safety shell** ("learning inside a stability-preserving structure"). Lane-based, homogeneous vehicles. |
| HC-STGRL 2026, Frontiers in AI, doi:10.3389/frai.2026.1891950 | **[P]** | Under 20% sensor failure it loses 25.4%, against 44.7% for CoLight. | Assumes lane-level detectors. |
| HALight 2026 | **[PP]** | Heterogeneous MARL with lane-level missing observations and one-hop communication. | One-hop messaging already exists, which supports never-claim #2. |
| Pei et al. 2026 (distributionally robust MARL) | **[PP]** | Optimises worst-case queue (Monaco network). | Worst-case reporting is emerging, but not in mixed traffic. |
| Lee & Chiu 2020, Sensors, doi:10.3390/s20020508 | **[P]** | **Field-tested** emergency-vehicle preemption with a "traffic flow compensation" stage after preemption. | **Prior art for recovery.** Confirms the never-claim "novel ambulance recovery". |
| Jiang 2026 (CPC meta-RL after emergencies), PLOS ONE, doi:10.1371/journal.pone.0357779 | **[P]** | Explicit disturbance term for regular traffic after an emergency. | Recovery is also published inside RL. |
| Dai et al. 2025, PLOS ONE, doi:10.1371/journal.pone.0323209 | **[P]** | Survey and model work: most preemption models handle **one** emergency vehicle. | Multiple emergency vehicles is a stated gap. |
| TrafficGen 2026, Frontiers in AI | **[P]** | Includes recovery from false alarms. | — |
| Su 2022 "EMVLight" (TR-C 2023) | **[P]** | Multi-agent RL for emergency-vehicle routing plus signal control. | Lane-based, homogeneous vehicles. |
| Su 2026 (Decision Transformer preemption) | **[PP]** | Trades emergency-vehicle travel time against civilian delay. | — |
| Roy et al. 2026 "MLEVP" | **[PP]** | Calibrated Vissim corridor. Limits the impact on conflicting movements. | — |
| Humagain & Sinha 2021 | **[PP]** | Preemption with mixed-criticality priorities. | — |
| Satheesh 2025 "MAPPO-LCE" | **[PP]** | Its future work lists mixed vehicle types and hard constraints. | Its authors admit Saarathi's Part B area is open. |
| Raeis 2021 | **[PP]** | Fairness metrics for TSC. | — |

---

## 2. The bigger gaps (ranked)

Ranking uses three tests: is the gap real across the published record, can a final-year team test it inside v5 scope, and does it stay clear of the never-claim list.

### BG1 — Do controller rankings survive the uncertainty of Indian traffic parameters? *(G6, strongly expanded)* — **rank 1**

- **Evidence**
  - PCU values are site-specific and code-book values are biased (Sugiarto 2021, 2024, 2025 **[P]**).
  - Rankings change across MDP families (Jayawardana **[PP]**).
  - Ranking preservation is now studied directly (LightSim **[PP]**).
  - **No TSC paper, Indian or not, tests whether "max-pressure beats actuated beats fixed" still holds when PCU values, two-wheeler share or sublane parameters move inside their published ranges.**
- **Why it is bigger than G6:** G6 asked only about PCU. The real gap covers the whole *calibration-uncertainty envelope*: PCU, vehicle mix, `lcSublane`/`minGapLat`, and demand.
- **Saarathi fit:** cheap. It needs only the existing baselines and seeds, swept across a parameter grid. Report rank agreement (Kendall τ) and the fraction of runs in which each ranking holds.
- **Safe claim:** "first systematic ranking-robustness study for Bengaluru-inspired mixed traffic in open SUMO". Keep it scoped. Do not write "first Indian".

### BG2 — No statistically rigorous Indian TSC evaluation *(G2, expanded)* — **rank 2**

- **Evidence**
  - Single-run practice (Riehl **[PP]**) and the statistical precipice (Agarwal **[P]**).
  - Chaudhuri **[P]** reports no seeds. Nandakumar **[PP]** reports point improvements.
  - SIGMA **[PP]** is the only Indian work with bootstrap statistics, on four junctions.
  - Saarathi's own `PART_A_DEEP_ANALYSIS.md` already found that the **5-seed rankings are not significant**, and that the CSVs contain duplicate rows.
- **The gap:** no Indian benchmark ships CIs, IQM, worst-seed results and paired tests *as the default output*.
- **Saarathi fit:** this is mostly reporting code. It is also **mandatory before any claim**, because current Saarathi numbers would fail this bar. Increase seeds until the CIs separate, or report the result as "no significant difference" honestly.

### BG3 — Sensing models for laneless traffic do not exist *(G1, expanded)* — **rank 3**

- **Evidence:** Sim2Signal, HALight, HC-STGRL and Com-MP all degrade or drop *lane-level detector* readings. In laneless traffic there are no lanes to put detectors on.
- **The gap:** what does a controller actually observe at a Bengaluru junction? Options include an approach-level camera PCU estimate, stop-line occupancy, aggregate counts, or nothing. How do the rankings change across these tiers?
- **Saarathi fit:** the parked "sensing tiers" axis already matches this. Implement it as *observation wrappers* over the same SUMO state: full sublane state, approach PCU with noise, approach count only, and time-of-day only.
- **Neighbour to cite and separate from:** Sim2Signal's observation gap. The difference is that its noise model is lane-based.

### BG4 — Max-pressure has never been fairly tested in Indian laneless SUMO *(new)* — **rank 4**

- **Evidence**
  - Nandakumar **[PP]** and Chaudhuri **[P]** both omit max-pressure.
  - Saarathi's own result shows PCU max-pressure clearly winning (46.5 s against 69.4 s for fixed). That suggests the Indian RL results may be inflated by weak baselines.
- **The gap:** a PCU-weighted max-pressure baseline under sublane dynamics, compared with RL, with the same seeds and metrics.
- **Saarathi fit:** already built. This is the most *defensible* headline: "a strong classical baseline that Indian RL papers omit".
- **Caution:** do not claim to beat Nandakumar. Different junction, different metric.

### BG5 — No open, licensed, multi-junction, field-anchored Indian benchmark *(G3 + G5 merged)* — **rank 5**

- **Evidence**
  - Every Indian study covers one junction (Chaudhuri, Nandakumar) or four (SIGMA).
  - Nandakumar's repo is unlicensed. Sadat **[P]** calibrates but does no control.
  - Calibration of laneless car-following exists only as preprints and only for Chennai (Kulkarni, Eldhose).
- **The gap:** all three properties at once — an open licence, multiple junctions with a plug-in controller API, and at least a partial field anchor.
- **Saarathi fit:** Studio plus `make_area.py` covers "multi-junction" and "open" today. **Field counts are still zero.** Without even one counted junction, the "field-anchored" part fails and the claim drops to "Bengaluru-inspired".

### BG6 — Emergency-vehicle handling in laneless traffic, and a standard disruption-cost metric *(Part B, new)* — **rank 6**

- **Evidence**
  - Recovery and compensation are prior art: Lee & Chiu 2020 **[P]** field-tested, Jiang 2026 **[P]**. So recovery itself is **not** a gap, which confirms the never-claim.
  - What *is* open:
    - (a) multiple emergency vehicles (Dai 2025 **[P]** says so explicitly);
    - (b) corridor clearance when two-wheelers filter into the gap, so that green time alone does not clear the path. No paper models this.
    - (c) no agreed metric for disruption to the cross street. Each paper defines its own.
- **Saarathi fit:** Part B is parked. When it returns, propose (c) as a *reported metric* (extra vehicle-hours on non-EV movements until queues return to the pre-event baseline) and present it as standardisation, not novelty.

### BG7 — Safety shells and stability-preserving RL have only been shown in lane-based traffic *(Part B, new)* — **rank 7**

- **Evidence:** Com-MP **[PP]** is the closest work, and it is lane-based and homogeneous. MAPPO-LCE **[PP]** lists hard constraints and mixed vehicle types as future work.
- **The gap:** does a shell such as min/max green, all-red and a max-pressure fallback keep its guarantees when "queue" becomes PCU-weighted and the dynamics are sublane?
- **Saarathi fit:** the Part B safety shell. Frame it as "Com-MP-style safety in mixed traffic" and **cite Com-MP**. Do not claim a new safe-RL method.

### BG8 — Two-wheeler filtering is not modelled by any TSC benchmark *(new, from the internal analysis plus literature)* — **rank 8**

- **Evidence**
  - Mode-dependent lane discipline (Anagnostopoulos **[PP]**).
  - Two-wheeler pairs show the most variability (Eldhose **[PP]**).
  - SUMO sublane is not validated for this (Lopez **[P]**).
  - The internal analysis shows Saarathi has no filtering yet.
- **The gap:** the effect that matters most for Indian junctions is missing from every simulator-based TSC study found.
- **Saarathi fit:** hard to do properly. At minimum, *state it as a threat to validity*, and run a sensitivity check with a two-wheeler `latAlignment`/`minGapLat` variant (this feeds BG1).

---

## 3. What does NOT count as a gap (checked against the never-claim list)

- "First Indian RL TSC": Chaudhuri 2022 **[P]** exists, as do Nandakumar and SIGMA **[PP]**.
- "Learned communication": HALight and CoLight already have neighbour messaging.
- "Ambulance recovery": Lee & Chiu 2020 **[P]** and Jiang 2026 **[P]**.
- "Digital twin" or "deployment": Saarathi has no field loop.
- "Beats BATCS": nothing to compare against.

---

## 4. Recommended order (proposals only, no scope change)

1. **BG2 first.** Fix duplicate CSV rows, add CIs, IQM, worst seed and paired tests, and raise the seed count. Everything else rests on this.
2. **BG4.** It is already built, so write it up as the strong-baseline result.
3. **BG1.** Run a parameter-envelope sweep and report rank stability. Low cost and the highest paper value.
4. **BG3.** Add sensing-tier observation wrappers. This links naturally to the parked "traffic cop vs signal" paper idea; that idea stays parked until the user returns to it.
5. **BG5.** Count at least one junction to move from "inspired" to "anchored".
6. **BG6, BG7 and BG8:** for when Part B is un-parked.

## 5. Threat watch

- **Nandakumar et al. (arXiv:2509.21745).** It was updated on 2026-11-03. If it is published, avoid every "open laneless SUMO framework" claim and position Saarathi as *multi-junction + max-pressure + rigour + ranking-robustness*.
- **sumoITScontrol and Sim2Signal.** These are the closest benchmark neighbours in method. Cite both and set Saarathi apart on heterogeneity and laneless sensing.

---

## 6. Addendum (2026-11-24): after reviewing Codex's work

Sources reviewed:
- commits `ceb5300`, `199b57e`, `73e563d`;
- `PART_A_DEEP_ANALYSIS.md` (F1–F7);
- `JOINT_PUBLICATION_STUDY.md`;
- `SAARATHI_MARKET_GAP.md`;
- `pune_dataset_check/`;
- `PART_A_LIT_GAP_REVIEW.md` (T3).

Codex's sources are taken as reported. I did not re-read them.

### 6a. Corrections to sections 2–5

- **BG8 (two-wheeler filtering) is weaker than I said.**
  - Guin et al. 2026, *Computer Networks* **[P]**, already does field-calibrated two-wheeler seepage in SUMO. Its baseline is 132 events with stock SUMO.
  - Codex built a `filtering` profile (A-014) and a direct same-lane seepage metric. Seepage is about 3.2–3.3× stock SUMO, and the lane-model ablation shows none.
  - The gap is now narrower: *nobody checks whether filtering changes which signal controller wins*. Codex's data hints that it does. Filtering cut fixed-time delay from 66 s to 36 s at Silk Board 0.8, and the delay effect flips with demand.
- **BG4 (max-pressure omitted) is overstated.**
  - EquiFlow, GIJET 2026 **[P]**, covers 4 Hyderabad junctions with mixed traffic, PPO, emergency priority *and* max-pressure. On one held-out run, fixed-time beat both PPO variants. Max-pressure used different transition handling there.
  - Agarwal et al., *Expert Systems with Applications* 2024 **[P]**, applies pressure control to heterogeneous traffic.
  - Restated gap: **a *tuned* PCU max-pressure, run with *the same* clearances, transitions and seeds as every other controller**, is still missing.
- **BG5:** add EquiFlow (4 junctions, no licensed release found) to the Indian list.
- **BG2 is now urgent, not theoretical.** Codex's own Welch tests found:
  - Domlur maxp vs fixed: t ≈ 0.95, not significant.
  - Silk Board 0.6: t ≈ 0.65, not significant.
  - Silk Board 0.6 is almost uncongested, so every controller looks the same there.

### 6b. New gaps

**BG9 — The value of measurement: which field data actually changes the decision?** *(from Codex's joint study; new and strong)*
- Every calibration paper asks "does the simulator match the counts?". None asks "would measuring *X* make us pick a different controller?".
- Proposed metric: **simulation-estimated decision loss**. This is the extra delay a city incurs if it picks a controller using a cheaper calibration. Compare aggregate counts only against counts plus platoon arrival timing, on held-out days.
- Prior art on platoon dispersion in Indian arterials exists (ASCE JTE **[P]**; Chennai field study, Procedia **[P]**). Prior art that links it to a control decision does not.
- The result is publishable even if a simple fixed plan wins.

**BG10 — Failed runs are hidden.** *(from Codex F2)*
- At Domlur, 8–52% of vehicles never finish, and there are 17–25 teleports and 3–9 collisions per run. Delay is cut off at sim end, so it *under*-states gridlock.
- No TSC benchmark found reports, per controller, the share of failed or censored runs together with delay.
- Gap: a validity rule, for example "a run with teleports above a threshold counts as failed". Report the failure rate per policy as a result in its own right.

**BG11 — There is no neutral pre-purchase test for cities.** *(from Codex market note; hypothesis only)*
- BATCS has about 103 adaptive junctions in Bengaluru, with no independent published performance numbers found. Vendors claim "built for Indian traffic" but publish no benchmark.
- Gap: race a vendor or student controller **against the city's own current signal plan** on the city's own junction, with an audit-style report card.
- This is a product gap, not a research gap. It explains *why* Part A matters.

**BG12 — The calibration data does not fit the model.** *(from the Pune check)*
- The only open Indian count set found is Pune, CC BY 4.0. It has 4 classes and no autos. Its directions are on-screen, not turning movements. Two-wheelers are under-counted.
- Gap: there is no open Indian dataset with turning movements by vehicle class plus signal timings, which SUMO calibration needs.
- A small Bengaluru count, released openly, would itself be a contribution.

### 6c. Final ranked list (merged)

1. BG2 statistics, plus BG10 failed-run honesty. This is the foundation, and current numbers fail it.
2. BG1 ranking robustness under parameter uncertainty (PCU, mix, filtering on/off).
3. BG9 value of measurement (decision loss).
4. BG3 sensing tiers for laneless traffic.
5. BG4′ tuned, matched PCU max-pressure as the honest bar.
6. BG5 + BG12 open, licensed, multi-junction benchmark with a small open Bengaluru count.
7. BG7 safety shell in mixed traffic (Part B).
8. BG6 emergency-vehicle cost metric in laneless traffic (Part B).
9. BG8′ does filtering change the controller ranking? (folds into BG1)
10. BG11 city own-plan baseline and report card (product framing)
