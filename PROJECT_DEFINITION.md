# Saarathi — Final Project Definition (v6, 2026-11-24)

> **This is the authoritative definition of Saarathi.** If another document disagrees, this document and `FINAL_PLAN.md` take priority. The full reasoning, sources, timeline and pitch are in `research/FINAL_GOAL.md`. The published-work overlap check is in `LITERATURE_AUDIT.md` and `research/DEEP_GAP_REVIEW.md`.

## In one sentence

**Saarathi is a fair, open SUMO test track for traffic-signal controllers in lane-less Indian mixed traffic, together with a safe learning controller raced on it that also measures what ambulance priority costs everyone else.**

## The real problem

1. **City claims can't be checked.** Indian cities buy adaptive signals without an open, fair way to test them. Bengaluru's BATCS claims 15–33% less travel time, but publishes no method, baseline or data.
2. **Standard tests don't fit Indian traffic.** Standard signal-control tests assume lane discipline, while most Bengaluru vehicles are two-wheelers that filter through gaps. A controller's ranking may not survive that change.
3. **Ambulance priority has an unmeasured cost.** Nobody publishes how much ambulance priority delays other traffic, or how long junctions take to recover.

## The project has two parts (one paper)

### Part A — the test track (the core contribution)
- Real Bengaluru OSM areas: the Old Airport Road signal pair, Silk Board, Trinity and Domlur. Mixed vehicles, sublane filtering, and load measured in **PCU**.
- One shared protocol for every controller: the same routes, seeds, warm-up, demand cut-off and drain time.
- Honest statistics: paired seeds, 95% confidence intervals, completed/scheduled trips, and every failed run reported.
- A **robustness sweep** that asks whether the ranking changes when we vary bike filtering, PCU versus vehicle counts, or the PCU values.
- A field check: one Old Airport Road junction counted live by eye, with no video kept and one window held out. Open Pune counts (CC BY 4.0) serve as a second-city sanity check.

### Part B — Saarathi, the safe controller (raced on Part A)
- **The PPO agent picks between safe rules:** local max-pressure, or max-pressure plus the incoming platoon from a neighbour. It never sets raw signal phases.
- **A hard safety shell** always enforces minimum and maximum green, yellow and all-red.
- **Neighbour messages:** PCU released, arrival time and an ambulance flag.
- **Ambulance mode** reports ambulance travel time, the extra delay to other traffic and the recovery time.
- Training happens in simulation only. We train on 3 areas and test on a 4th it never saw.

**Either result is publishable.** If Saarathi wins, it is shown fairly. If it ties or loses, the reason is still new evidence for Indian traffic.

## Research questions
1. How do fixed-time, actuated and PCU max-pressure rank under lane-less mixed traffic, with honest statistics?
2. Does the ranking change when bike filtering, PCU values or demand change?
3. Does the safe AI selector beat tuned max-pressure, including on an unseen area?
4. What does ambulance priority cost other traffic, and how fast do junctions recover?

## Controllers compared
Fixed-time (city-style plan), actuated, tuned PCU max-pressure, message-aware max-pressure with no AI, and Saarathi. Comparing the last two separates the gain from messages from the gain from learning.

## Honest project claim

> We release a fair, reproducible SUMO benchmark for lane-less Indian mixed traffic. On it, we test whether controller rankings survive those assumptions, evaluate a safe learning controller against tuned max-pressure, and measure the cost of ambulance priority. All results are from simulation only.

**Never claim:** a first Indian simulator or AI, that we beat BATCS, a digital twin, deployment, a novel safety shell, novel learned communication, or novel ambulance recovery.

## Not core
Dashboards, city scale, nightly retraining, fairness modules, sensor-failure modules and live deployment. Sensing tiers, a second field junction and Studio playback are allowed only after everything in `FINAL_PLAN.md` is done.

## Easy way to remember it

**Part A is the fair race track. Part B is our safe racer. The paper reports who wins, whether the result holds, and what ambulances cost.**
