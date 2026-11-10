# Saarathi — Final Build Plan (v5, locked 2026-11-10)

**Authority:** this plan and `PROJECT_DEFINITION.md` define the active project. Version mapping: `VERSION_HISTORY.md`.

## Goal

Build two things together:

1. an open, reproducible SUMO environment for Bengaluru-inspired Indian mixed, non-lane traffic; and
2. Saarathi, a safe decentralised controller whose junction nodes use PCU-based traffic information and neighbour messages to coordinate a configurable corridor.

## Required deliverables

| Part | Deliverable | Done when |
|---|---|---|
| A — Environment | Configurable SUMO corridor with sublane behaviour, Indian vehicle mix, PCU values, demand profiles, documented assumptions, and reproducible runs | Another person can clone the project, run the reference scenario, and obtain comparable metrics. |
| A — Benchmark | Fixed-time, Max-Pressure, and feasible MPLight/CoLight comparison adapters; common metrics and multiple seeds | Every controller is evaluated under identical demand and seeds. |
| B — Saarathi controller | PPO-controlled junction agent protected by the safety shell | It makes only safe phase decisions and is compared fairly with Max-Pressure. |
| B — Coordination | Node-to-node platoon messages: released PCU, ETA, emergency priority | The reference-corridor experiment compares independent control with coordinated control. |
| B — Ambulance | Route-ahead priority plus cross-street recovery metric | We report ambulance travel time and recovery time, not only ambulance speed. |
| Release | Code, scenarios, assumptions, results, and reproduce instructions | The project is usable as an open benchmark/demo. |

## Controller contract

Each junction is a node. It observes local PCU queues/arrivals and its legal signal state. It may receive messages from immediate neighbours. It requests a phase; the safety shell enforces minimum/maximum green, yellow, and all-red intervals. A node cannot make an unsafe switch.

## Evaluation claim

We report whether Saarathi reduces delay, stops, queueing, and emergency disruption **in this simulator** compared with the listed baselines. We make no real-world deployment or city-wide congestion claim.

## Build order

1. Finalise and document the environment; verify mixed traffic visually and with manual-count-informed assumptions.
2. Make the experiment runner reproducible; run Fixed-time and Max-Pressure across seeds.
3. Complete and evaluate PPO on one junction, then extend it to the corridor.
4. Add neighbour messaging; test green-wave benefit against independent nodes.
5. Add ambulance priority and cross-street recovery measurement.
6. Add external baselines only where they can be integrated fairly; publish results, report, and demo.

## Scope guardrails

- Reference network: **one configurable, field-verified corridor**; the final node count is chosen for credibility and feasibility, not novelty.
- Learning happens in simulation only.
- PCU is the common measure of road load.
- Nightly retraining, fairness, sensor failures, dashboard work, and city-scale expansion are optional extensions—not requirements for project completion.
