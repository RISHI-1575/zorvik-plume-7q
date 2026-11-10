# Saarathi — Related Papers (Historical Literature Collection)

This folder contains 22 papers/preprints gathered during earlier project versions. **It is not a vetted bibliography:** some files are arXiv versions and must not be called approved/published without checking their final venue. For the current scope, overlap analysis, and a verified-published reading list, use `../LITERATURE_AUDIT.md` first.

## A. Multi-Agent RL for Traffic Signal Control (the core)
- **04 — Chu et al. 2019, MA2C.** Multi-agent A2C for large-scale traffic signal control. Closest methodological baseline for a decentralized junction-agent design. `arXiv:1903.04527`
- **05 — Wei et al. 2019, Survey.** Survey of traffic-signal-control methods (fixed-time → RL). Use for the "why not SCATS/SCOOT" framing. `arXiv:1904.08117`
- **10 — Wei et al. 2019, CoLight.** ⭐ **Closest prior work.** Already uses **graph-attention networks** for neighbor cooperation in traffic signal control on hundreds of junctions. Cite this as the baseline your learned-communication claim must beat. `arXiv:1905.05717`

## B. Learned / Emergent Communication (the differentiator)
- **01 — Foerster et al. 2016, DIAL/RIAL.** Foundational: agents learn *what* to communicate via differentiable messaging. Direct basis for "hubs discover what to signal." `arXiv:1605.06676`
- **02 — Sukhbaatar et al. 2016, CommNet.** Learned continuous inter-agent communication. `arXiv:1605.07736`
- **08 — Lazaridou & Baroni 2020, Survey.** Emergent multi-agent communication — situates the emergent-protocol novelty claim. `arXiv:2006.02419`

## C. Architecture — Graph Attention
- **03 — Veličković et al. 2017, GAT.** The graph-attention mechanism itself. `arXiv:1710.10903`

## D. Multi-Objective & Equity (the differentiator)
- **09 — Hayes et al. 2022.** Practical guide to multi-objective RL — for the Pareto-frontier / multi-reward design. `arXiv:2103.09568`
- **13 — Raeis & Leon-Garcia 2021.** Deep RL for **fair** traffic signal control (delay- and throughput-based fairness). Prior art on fairness — your equity angle must go beyond per-vehicle fairness. `arXiv:2107.10146`

## E. Byzantine / Fault Tolerance (the differentiator — thinnest existing literature in traffic)
- **11 — Xu et al. 2023.** Byzantine-robust *cooperative* MARL as a Bayesian game. Closest to "neighbors self-compensate when a hub is compromised." `arXiv:2305.12872`
- **12 — Lin et al. 2021.** Resilient consensus-based MARL with function approximation. `arXiv:2111.06776`

## F. Cross-cutting MARL methods
- **06 — Foerster et al. 2017, COMA.** Counterfactual credit assignment for cooperative MARL. `arXiv:1705.08926`
- **07 — Lowe et al. 2017, MADDPG.** Centralized-training / decentralized-execution actor-critic. `arXiv:1706.02275`

## G. Simulator
- **14 — López et al. 2018, SUMO.** The reference paper for the SUMO simulator (supports the sublane model needed for lane-less Indian traffic). `DOI:10.1109/ITSC.2018.8569938`

## H. ⚠️ Same-topic / novelty-check (DIRECT overlaps — read these first)
These hit Saarathi's "novel" pillars head-on. They are why the original claims need reframing (see ../README.md).
- **15 — BARD-MARL 2026.** Byzantine-agent *detection for learned communication* in MARL — overlaps pillars 1 + 3 at once. `arXiv:2606.20701`
- **16 — Human-Centric TSC for Equity 2026.** MARL + **equity** in traffic signal control — overlaps pillar 2. `arXiv:2602.02959`
- **17 — Representational Communication for Large-scale TSC 2023.** Learned communication in traffic MARL — overlaps pillar 1. `arXiv:2310.02435`
- **18 — Constrained MARL for Autonomous TSC 2025.** Constraint-based (safety/priority) MARL traffic control. `arXiv:2503.23626`

## I. Robustness benchmarking prior art (Western traffic only — the gap Saarathi 2.0 fills)
- **19 — Robust DRL for TSC 2019.** Stress-tested RL signal control: demand surges, incidents, sensor failures. Single intersection, Western. `arXiv:1904.08353`
- **20 — Robustness under Incidents 2025.** Comparative robustness study of RL controllers. Western. `arXiv:2506.13836`
- **21 — Evaluating Robustness of RL ATSC 2026.** Newest robustness evaluation. Western. `arXiv:2603.15283` (Also see: T-REX and CAREL benchmark platforms — both Western.)

## J. India prior art
- **22 — Bengaluru comparison 2021.** DQN/A2C vs simple schedulers on ONE real Bengaluru intersection. No mixed-traffic depth, no robustness, no equity — shows how empty the India niche is. `arXiv:2109.00937`

## Must-cite baselines NOT yet downloaded (find implementations)
Max-Pressure control · PressLight · MPLight · FRAP · IntelliLight · MA2C · **RESCO** / **LibSignal** benchmarks · CityFlow. A reviewer will reject fixed-time-only comparisons.
