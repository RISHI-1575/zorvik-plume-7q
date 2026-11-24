# Saarathi — Final Build Plan (v6, locked 2026-11-24)

**Authority:** this plan and `PROJECT_DEFINITION.md` define the active project. The full reasoning, sources and pitch are in `research/FINAL_GOAL.md`. The version map is in `VERSION_HISTORY.md`.

## Goal

Build one paper's worth of evidence:
1. **Part A:** a fair, open SUMO test track for lane-less Indian mixed traffic.
2. **Part B:** Saarathi, a safe PPO controller that picks between max-pressure rules, raced on that track, with an ambulance-cost measurement.

## Required deliverables (must-have)

| # | Deliverable | Done when |
|---|---|---|
| A1 | Four real areas (Old Airport Road pair, Silk Board, Trinity, Domlur) under one protocol | Every controller runs with the same routes, seeds, warm-up, demand cut-off and drain time |
| A2 | Gridlock handled | Domlur is fixed or reported as a stress test, and every failed run is counted |
| A3 | Honest statistics | 10 paired seeds × 2 demand levels, 95% CIs and completed/scheduled trips for every result |
| A4 | Robustness sweep | Rankings are reported with filtering on and off, PCU versus vehicle counts, and a second PCU set |
| A5 | Field check | One Old Airport Road junction is counted live with no video kept, and the simulator is calibrated and then checked on a held-out window |
| A6 | Second-city check | The Pune CC BY 4.0 counts are used as a sanity check |
| A7 | Reproducible release | One command rebuilds the tables, versions are pinned, the work is committed and licensed, and it reruns on a teammate's laptop |
| B1 | Safety shell enforced for PPO | Maximum green is enforced on the PPO path (today `env.py` never calls `must_rotate()`), and a "hold forever" test passes |
| B2 | Safe AI selector | PPO picks between local max-pressure and max-pressure plus the neighbour's platoon, using one shared policy across all junctions |
| B3 | Neighbour messages | PCU released and arrival time are sent between neighbours, and message-aware max-pressure without AI is a separate baseline |
| B4 | Unseen-area test | The policy is trained on 3 areas and tested on the 4th, with 3 training seeds |
| B5 | Ambulance cost | Route-ahead priority is in place, and ambulance time, extra delay to others and recovery minutes are reported |

## Controller contract

- Each junction is a node. It observes local PCU queues and arrivals, and may receive neighbour messages.
- The PPO agent picks a **rule**, never a raw phase.
- The safety shell enforces minimum and maximum green, yellow and all-red on **every** controller path. No node can make an unsafe switch.

## Evaluation claim

We report, **in this simulator only**:
- whether the rankings survive our assumptions;
- whether Saarathi beats tuned max-pressure;
- what ambulance priority costs other traffic.

We make no deployment, "beats BATCS" or digital-twin claim.

## Build order (≈11 weeks, 3 people; details in `research/FINAL_GOAL.md` §7)

1. Week 1: commit everything, time one full paired run and fix B1. Choose the field junction and get the BGIT permission letter.
2. Weeks 2–3: A1 and A2, the live field count (A5), and B2/B3.
3. Weeks 4–5: A3, calibrate and check the field data (A5), the Pune check (A6), and B4.
4. Weeks 6–7: the A4 sweep, A7 reproduction, and B5.
5. Week 8: the final race, both tables and the figures.
6. Weeks 9–11: write the paper and submit it to the SUMO User Conference 2027 (deadline expected around mid-February 2027; check it when the call is out).

**If time runs out, cut in this order:** B5, then the 4th area, then A6. Never cut A3, B1 or the held-out window.

## Scope guardrails

- Learning happens in simulation only. PCU is the common measure of load, and raw class counts are kept beside it.
- Sensing tiers, a second field junction and Studio playback come only after every must-have item is done.
- Dashboards, city scale, retraining, fairness and sensor-failure modules are out of scope.
