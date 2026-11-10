# Saarathi

**Open Indian mixed-traffic simulator + safe decentralised traffic-signal controller.**

Saarathi has two parts: a reproducible, configurable Bengaluru-inspired SUMO corridor for Indian mixed/non-lane traffic, and our PCU-aware controller that lets neighbouring signals coordinate, form green waves, and prioritise ambulances safely.

## Start here

- **Final idea:** [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md)
- **Final build plan:** [FINAL_PLAN.md](FINAL_PLAN.md)
- **Version map:** [VERSION_HISTORY.md](VERSION_HISTORY.md)
- **Published-paper overlap audit:** [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md)
- **Current status + publication plan:** [PROJECT_STATUS_AND_PUBLICATION_PLAN.md](PROJECT_STATUS_AND_PUBLICATION_PLAN.md)
- **Simulator research + build checklist:** [SIMULATOR_RESEARCH_AND_BUILD_PLAN.md](SIMULATOR_RESEARCH_AND_BUILD_PLAN.md)
- **Current progress:** [PROGRESS.md](PROGRESS.md)

Final-year capstone — G9: Rishi Shashikanth · P Yukthesh · Vimal · BG Institute of Technology · 2025–26.

**Stack:** Multi-agent RL · emergent communication · graph attention networks · multi-objective optimization · SUMO · PyTorch · Ray RLlib · Python.

## Folder layout
```
Saarathi/
├── README.md                     ← this file
├── Saarathi-Capstone-Deck.pptx   ← 10-slide capstone presentation
├── papers/                       ← 14 related papers + indexed lit-review (see papers/README.md)
└── showcase/                     ← proposal showcase site (git repo → github.com/RISHI-1575/g9-project-showcase)
    └── index.html                ← Saarathi + AEGIS-X + Chakravyuh-2 comparison
```
Run the showcase locally: `cd showcase && python3 -m http.server 4321` → http://localhost:4321

> **⚠️ ARCHIVED BACKGROUND:** The analysis below belongs to the original broad project pitch. It is retained for literature/novelty history only. The current scope is [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md) and [FINAL_PLAN.md](FINAL_PLAN.md).

## Idea validation — verdict (literature scan + GPT-5.5 second opinion)

**Blunt finding: as pitched, all five "novelty" pillars already exist in the literature — some already combined, some already in traffic.** This is buildable, but a serious reviewer would call it an *incremental kitchen-sink integration* and reject it. Per-pillar:

| Pillar | Status | Closest existing work (in `papers/`) |
|---|---|---|
| Learned/GAT communication | **done** | CoLight (10), Representational Comms (17) |
| Multi-objective + equity | **done** | Human-Centric Equity TSC (16), Fair-traffic (13) |
| Byzantine / fault tolerance | **partially done** | BARD-MARL (15), FT-Attn-MADDPG, Xu (11), Lin (12) |
| Indian lane-less mixed traffic | **partially open** | only novel if you deliver a *calibrated* benchmark, not "bikes+autos in SUMO" |
| Baselines vs fixed-time/SURTRAC | **inadequate** | need Max-Pressure, PressLight, MPLight, MA2C, RESCO/LibSignal |

**Real-world impact as-is: simulation-only.** Real Indian junctions lack lane-level sensing; SUMO lane-less is an approximation; ambulance corridors and equity weights need legal/operational grounding, not reward hacks.

## The unique, publishable, high-impact reframe
Stop selling "a new GAT-MARL controller." The genuinely novel, executable (~6–9 mo), publishable contribution is a **robustness + equity BENCHMARK for Indian mixed-traffic signal control** with a **failure-aware safe controller**:

1. Build 2–3 SUMO networks modeled on real Indian junctions: heterogeneous vehicles, weak lane discipline (sublane), noisy/partial detectors, emergency routes, demand skewed across neighborhoods.
2. Define stress tests: junction failure, frozen/malicious messages, detector dropout, demand surge, emergency insertion, equity-skewed OD demand.
3. Benchmark strong baselines (Max-Pressure, PressLight/MPLight, CoLight, MA2C) + a simple **hybrid**: MARL in normal operation, local safe fallback + hard phase-safety + emergency-preemption constraints under anomaly.
4. **Claim:** "SOTA learned-communication TSC degrades sharply under realistic Indian mixed-traffic failures; a simple failure-aware constrained controller wins on worst-case delay, emergency response, and equity stability." — honest, measurable, useful.

**Realistic target:** solid workshop/demo paper (NeurIPS/ICLR/AAMAS/IEEE-ITSC workshop, ACM COMPASS if equity is serious). A full IEEE-ITSC/AAMAS/T-ITS paper is possible only with calibrated scenarios, strong baselines, multi-seed significance, and public code. The novelty lives in the *benchmark + robustness evidence*, not another controller.

> Full same-topic overlap list and must-cite baselines: see `papers/README.md` sections H and the baseline note.
