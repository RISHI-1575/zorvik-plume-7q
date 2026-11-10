# Saarathi — Final Project Definition (v5, 2026-11-10)

> **This is the authoritative definition of Saarathi.** If another document disagrees, this document and `FINAL_PLAN.md` take priority.

The published-work overlap check and paper-safe positioning are in `LITERATURE_AUDIT.md`.

## In one sentence

**Saarathi is an open, Bengaluru-inspired SUMO test environment for Indian mixed, non-lane traffic, together with our safe decentralised traffic-signal controller that coordinates neighbouring junctions, creates green waves, and prioritises ambulances.**

## The project has two equal parts

### 1. Open Indian mixed-traffic simulation environment

We build and release a reusable **configurable road-corridor simulator**. The first reference scenario may contain four or another manageable number of verified signalised nodes; the architecture is not tied to that number. It represents Indian road conditions more realistically than ordinary lane-disciplined benchmarks:

- mixed vehicles: two-wheelers, autos, cars, buses, and trucks;
- weak lane discipline / filtering using SUMO's sublane model;
- vehicle load measured in **PCU** (Passenger Car Units), not merely vehicle count;
- Bengaluru-inspired demand and signal assumptions, checked against manual counts where possible;
- repeatable scenarios, seeds, metrics, and baseline controllers.

**Why this matters:** other researchers can run their signal-control method in the same Indian mixed-traffic setting and compare results fairly. It is a simulation benchmark, not a claim that we have recreated Bengaluru exactly.

### 2. Saarathi's decentralised signal controller

On top of that environment, we build our own controller:

- every junction is a **node/agent** with its own traffic state;
- nodes use PCU-based queues and arrivals to decide safe signal phases;
- each node sends neighbouring nodes a small message: how much traffic it released, its expected arrival time, and whether it is an emergency;
- these messages help adjacent signals time their greens, forming a corridor-level **green wave**;
- an ambulance message travels ahead so junctions clear its route, then the controller measures how quickly cross streets recover;
- a hard safety layer always enforces minimum/maximum green, yellow, and all-red timings.

The learning component is PPO. It is trained and evaluated **inside the simulator**; Saarathi does not learn by experimenting on real road users.

## What we will prove

We will compare fixed-time control, Max-Pressure, and feasible external baselines such as MPLight/CoLight against Saarathi in the same scenarios. The evidence will use:

- average delay and travel time;
- stops per vehicle;
- queue/spillback;
- ambulance travel time;
- cross-street recovery time after ambulance priority;
- results across multiple random seeds.

## Honest project claim

> In a Bengaluru-inspired, non-lane mixed-traffic simulation, Saarathi's safe, decentralised PCU-aware controller coordinates neighbouring junctions and can be evaluated fairly against established traffic-signal baselines.

We claim **simulation results only**. We do not claim to have solved Bengaluru congestion, built a live deployable system, recreated a city-wide digital twin, or invented the first RL traffic controller for India.

## Concrete scope

- **Network:** one configurable corridor as the reference benchmark; its final node count follows the selected and field-verified layout, not a hard-coded project requirement.
- **Environment:** SUMO + sublane traffic; open code, scenarios, and reproduction instructions.
- **Controller:** fixed-time and Max-Pressure are complete; PPO hub/agent, neighbour messaging, ambulance priority, and recovery measurement are the remaining core work.
- **Not core:** city-scale modelling, a live dashboard, fairness optimisation, sensor-failure modules, and nightly continual retraining. These remain optional only after the two-part core is complete.

## Easy way to remember it

**Part A builds the road world everyone can test on. Part B builds Saarathi, the traffic-signal brain that operates inside that world.**
