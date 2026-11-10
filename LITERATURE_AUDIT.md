# Saarathi — Published Literature Audit and Paper Positioning

**Audit date:** 2026-11-10  
**Rule:** this audit distinguishes peer-reviewed/published work from preprints. Do not present an arXiv manuscript as an approved publication unless its final venue can be verified.

## Executive verdict

Saarathi is a valid capstone and can become a clear paper, but **not** as a new MARL algorithm. The literature already covers every individual controller feature we previously described:

- decentralised multi-junction RL;
- learned/attention-based inter-junction communication;
- green-wave/arterial coordination;
- Indian heterogeneous traffic and PCU-based RL;
- ambulance priority and traffic recovery after pre-emption;
- open traffic-signal libraries and benchmarks.

The defensible paper is therefore:

> **A reproducible, Bengaluru-inspired 4-junction SUMO benchmark for mixed, weak-lane-discipline traffic, with a PCU-aware reference controller and a transparent evaluation protocol.**

Saarathi's controller is useful as the **reference method and demonstration**, not the paper's claimed algorithmic novelty.

## What we can and cannot claim

| Proposed element | Existing published work | Audit result | Safe wording |
|---|---|---|---|
| Open TSC benchmark/library | RESCO; LibSignal; CityFlow | Existing field; it is not novel to release an open TSC environment. | “An open benchmark scenario for Indian mixed traffic.” |
| Decentralised RL per junction | MA2C, CVLight, many MARL TSC papers | Established. | “A decentralised reference controller.” |
| Attention/learned communication | CoLight; Bokade et al. | Direct overlap. Do not claim learned communication as novel. | “Explicit adjacent-node messages, chosen for interpretability and reproducibility.” |
| Coordination / green waves | PressLight, CoLight, conventional coordinated control | Established. | “We measure coordination in a mixed-traffic corridor.” |
| PCU-aware Indian mixed-traffic RL | Savithramma & Sumathi (2023); Agarwal et al. (2024) | Direct overlap, including PCU state and Indian intersections. | “PCU-aware evaluation in a multi-junction open scenario.” |
| Ambulance pre-emption | EMVLight and a large EVTSP literature | Established. | “An optional benchmark scenario.” |
| Cross-street recovery after ambulance | Qin & Khan (2012); Kiani & Saraç (2023); later EVTSP work | Direct overlap. It is a good metric, not a new concept. | “We report recovery consistently in our benchmark.” |
| Safety min/max green, yellow, all-red | Standard traffic engineering; constrained TSC research | Necessary engineering, not a research contribution. | “A safety wrapper used for all learned methods.” |
| ‘First Indian RL’ / ‘first open Indian environment’ | Cannot be established from a literature search; India-focused papers exist. | Do not claim. | “We release a Bengaluru-inspired scenario and document its assumptions.” |

## The final paper contribution set

Keep only the following four contributions. They are simple to write, test, and defend.

1. **Scenario contribution:** an openly released, reproducible, 4-junction SUMO corridor for Indian heterogeneous traffic. It contains documented vehicle mix, sublane settings, PCU assumptions, signal plans, demand profiles, random seeds, and manual-count checks.
2. **Protocol contribution:** one fair harness that runs every controller under identical demand, seeds, warm-up, metrics, and safety constraints. The protocol reports uncertainty, not a single best run.
3. **Evidence contribution:** a controlled study of what changes under (a) lane-disciplined vs sublane traffic, (b) vehicle-count vs PCU-based state/pressure, and (c) independent vs explicitly coordinated junction control.
4. **Reference-controller contribution:** Saarathi is an interpretable decentralised PPO controller. Its only explicit messages are `released PCU`, `ETA`, and `emergency flag`; the same safety shell is applied to all methods. This makes it a reproducible reference implementation, not a claim of a new MARL architecture.

The ambulance scenario is best presented as a **fourth evaluation scenario** with two metrics—ambulance travel time and post-pre-emption cross-street recovery—not as a separate novelty claim.

## Recommended paper title and central claim

### Best title

**Saarathi: A Reproducible SUMO Benchmark for Bengaluru-Inspired Mixed-Traffic Signal Control**

### Alternative title

**Evaluating Decentralised Traffic-Signal Control under Indian Mixed Traffic: An Open 4-Junction SUMO Benchmark**

### Claim to defend

> We introduce and release a reproducible, Bengaluru-inspired SUMO benchmark that makes Indian heterogeneous, weak-lane-discipline traffic explicit, and use it to evaluate conventional and decentralised traffic-signal controllers under a common protocol.

This is deliberately narrower than “Saarathi solves Indian congestion.” It is credible if the scenario calibration and release are real.

## Required experimental matrix

| Question | Comparison | Result to report |
|---|---|---|
| Does the benchmark matter? | Same controller: lane-disciplined vs SUMO sublane/mixed traffic | delay, stops, queue, throughput; explain the change |
| Does PCU matter? | vehicle-count Max-Pressure / PPO vs PCU-weighted versions | system metrics plus per-vehicle-class outcomes |
| Does coordination matter? | independent PPO vs Saarathi explicit-neighbour PPO | stops, corridor travel time, queue/spillback; message ablation |
| Does emergency handling disrupt others? | no priority / conventional pre-emption / Saarathi priority | ambulance travel time, total delay, cross-street recovery time |
| Are results robust? | at least 5 seeds × weekday demand profiles × demand levels | mean, standard deviation or 95% CI, and raw data |

**Minimum baselines:** fixed-time, actuated, tuned Max-Pressure, and one established RL baseline that can genuinely run under the same SUMO network. Add PressLight/MPLight/CoLight only after verifying an implementation is adapted fairly. A broken or lightly tuned external baseline is worse than omitting it and stating the limitation.

## Published core literature to cite

These are the papers that should form the paper's Related Work section. They are published venues/journals, not merely pending manuscripts.

### Benchmarks and simulators

1. **Lopez et al. (2018), SUMO 2018.** The SUMO simulator reference. DOI: [10.1109/ITSC.2018.8569938](https://doi.org/10.1109/ITSC.2018.8569938).
2. **Zhang et al. (2019), CityFlow.** Large-scale MARL traffic-simulation environment. DOI: [10.1145/3308558.3314139](https://doi.org/10.1145/3308558.3314139).
3. **Ault & Sharon (2021), RESCO.** Open SUMO reinforcement-signal-control benchmark. [OpenReview paper](https://openreview.net/forum?id=LqRSh6V0vR).
4. **Mei et al. (2024), LibSignal.** Cross-simulator library and fair-comparison framework. DOI: [10.1007/s10994-023-06412-y](https://doi.org/10.1007/s10994-023-06412-y).

### Decentralised and coordinated traffic-signal control

5. **Chu et al. (2020), MA2C.** Decentralised multi-agent A2C, evaluated on synthetic and Monaco networks. DOI: [10.1109/TITS.2019.2901791](https://doi.org/10.1109/TITS.2019.2901791).
6. **Wei et al. (2019), PressLight.** RL grounded in max-pressure for arterial coordination. DOI: [10.1145/3292500.3330949](https://doi.org/10.1145/3292500.3330949).
7. **Wei et al. (2019), CoLight.** Graph-attention communication for network-level signal cooperation. DOI: [10.1145/3357384.3357902](https://doi.org/10.1145/3357384.3357902).
8. **Bokade, Jin & Amato (2023).** Representation-based selective inter-agent communication for large-scale TSC. DOI: [10.1109/ACCESS.2023.3275883](https://doi.org/10.1109/ACCESS.2023.3275883).
9. **Mo et al. (2022), CVLight.** Decentralised RL for multi-intersection control with connected-vehicle data. DOI: [10.1016/j.trc.2022.103728](https://doi.org/10.1016/j.trc.2022.103728).

### Indian / heterogeneous traffic and PCU

10. **Savithramma & Sumathi (2023).** RL controller for heterogeneous traffic at a Tumakuru, Karnataka intersection; explicitly compares vehicle-type, PCU, and multi-agent representations. DOI: [10.1016/j.geits.2023.100124](https://doi.org/10.1016/j.geits.2023.100124).
11. **Agarwal et al. (2024).** Hybrid Max-Pressure + PPO for heterogeneous traffic using video-derived demand at a Ludhiana intersection. DOI: [10.1016/j.eswa.2024.124416](https://doi.org/10.1016/j.eswa.2024.124416).
12. **Padinjarapat & Mathew (2021).** Saturation-flow estimation for non-lane-based mixed traffic streams, directly relevant to calibrating the environment rather than treating PCU values as universal constants. DOI: [10.1080/21680566.2020.1781708](https://doi.org/10.1080/21680566.2020.1781708).

### Emergency priority and recovery

13. **Qin & Khan (2012).** Emergency pre-emption transitions and recovery to normal operation. DOI: [10.1016/j.trc.2012.04.004](https://doi.org/10.1016/j.trc.2012.04.004).
14. **Su et al. (2023), EMVLight.** Decentralised RL for joint emergency routing and signal control. Published in *Transportation Research Part C*. DOI: [10.1016/j.trc.2022.103955](https://doi.org/10.1016/j.trc.2022.103955).
15. **Kiani & Saraç (2023).** RL-based traffic recovery after emergency passage. DOI: [10.1016/j.ins.2022.11.057](https://doi.org/10.1016/j.ins.2022.11.057).

## Items that must not be used as “approved-paper” evidence yet

The local folder contains several papers that are explicitly arXiv versions or have no verified final venue in the document itself (for example the constrained-MARL, robustness, human-centric equity, BARD-MARL, and some 2025/2026 papers). They are useful background, but label them **preprints** unless a final peer-reviewed record is checked before writing the paper.

The existing `papers/README.md` says “14 papers” but contains 22 PDFs and mixes published work with preprints. This audit supersedes that wording for paper-writing purposes.

## What to remove from the final paper and slides

- “First RL for Indian traffic.”
- “First open environment for Indian non-lane traffic.”
- “Novel learned communication / GAT communication.”
- “Novel ambulance recovery.”
- “Digital twin of Bengaluru.”
- “Beats BATCS” unless the actual BATCS software/configuration is evaluated under a disclosed and fair protocol.
- Any promise of real-world deployment or live online learning.

## What makes the benchmark credible

The contribution fails if the environment is only “bikes added to SUMO.” Include a `docs/assumptions.md` and release:

1. source or manual-count basis for modal split and hourly volumes;
2. PCU factors, their source, and a sensitivity test (fixed PCU values are an assumption, not ground truth);
3. SUMO car-following, lane-changing, and sublane settings;
4. signal phase plans, intergreen settings, and detector/observation model;
5. network source and every manual network edit;
6. generated routes, seeds, controller hyperparameters, and raw results;
7. a one-command reproduce script.

## Recommended paper outline

1. **Introduction:** existing benchmark environments insufficiently expose Indian heterogeneous/non-lane assumptions; do not overclaim absence of all Indian work.
2. **Related work:** benchmarks, coordinated RL, Indian heterogeneous traffic, emergency pre-emption/recovery.
3. **Benchmark design:** network, traffic model, PCU, calibration evidence, and reproducibility package.
4. **Reference controller:** local observation, explicit messages, safety shell; no claim of a new RL algorithm.
5. **Evaluation protocol:** controllers, demand scenarios, seeds, metrics, statistical reporting.
6. **Results:** benchmark sensitivity first; controller comparison second; ambulance scenario third.
7. **Limitations:** simulation-only, one corridor, imperfect behavioural calibration, no live deployment inference.
8. **Release:** exact repository artefacts and licence.

## Final decision

**Proceed, but reposition.** The best and easiest-to-write paper is an open-environment/evaluation paper with a reference controller. Do not attempt to sell a new PPO/MARL/communication/ambulance algorithm. The strongest possible result is not “our AI is globally best”; it is “the community can now reproduce and compare signal-control methods under disclosed Indian mixed-traffic assumptions, and here is a transparent reference result.”
