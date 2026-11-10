# Saarathi — Archived Project Spec (v4, 2026-07-10)

> **ARCHIVED — do not use this document as the current project scope.** It records the v3/v4 self-learning-hub design. The active, final definition is [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md); the executable scope is [FINAL_PLAN.md](FINAL_PLAN.md). See [VERSION_HISTORY.md](VERSION_HISTORY.md) for why this changed.

*Direction validated through: 22-paper scan (`papers/`) + web sweeps on BATCS, Taiwan signals, emergency preemption + two GPT-5.5 reviews. This is the single source of truth; earlier versions are superseded.*

---

## 1. The idea in one line
> **Saarathi — a self-learning traffic signal for each Indian junction. Every junction has its own agent (a "hub") that learns *that* junction's daily traffic rhythm — by time of day, day of week, and live conditions — treats all vehicles as one mixed flow, keeps getting better every day, and coordinates with neighbouring signals to form green waves. Software-only, on the signals already installed.**

## 2. The heart of the system — a self-learning hub per junction
1. **One agent per junction, tailored to that junction.** It is not a city-wide brain and not a one-size-fits-all model. Each junction grows its *own* controller from its *own* traffic. A quiet residential junction and a chaotic market junction end up with different learned behaviour.
2. **It learns the junction's daily rhythm.** The agent's decisions depend on time-of-day and day-of-week, so it acts differently at the 9 am peak, the 2 pm lull, and 11 pm — because it has learned what that junction *usually* looks like at each time.
3. **It keeps learning every day (continual).** It is never "finished." Each day's traffic refines it, so it adapts as patterns drift — a new mall opens, road works appear, festival season hits. The junction effectively builds a living memory of its traffic.
4. **It learns safely, not by gambling on live cars.** Pure trial-and-error on a real signal would cause real jams. So the agent learns and tests inside a **digital twin** of its junction (a SUMO model fed by that day's real counts), and only the *improved, validated* timing is pushed to the real signal. Learn in simulation → deploy safe → repeat nightly.
5. **Mixed traffic counted as one flow (PCU).** No bike-vs-car classification. Vehicles are measured in **Passenger Car Units** (a bike ≈ 0.25–0.5 of a car) so the signal senses true road-space pressure without having to identify every vehicle. Simple, robust, matches Indian reality.

## 3. The coordination layer — junctions talk, green waves form
6. **Neighbour messages.** When a batch of traffic leaves a junction, it tells the next junction *how much is coming and when*. The next signal opens green in time to catch it. Chain this across a corridor → you ride a run of greens and **stop once instead of ten times**.
7. **Commit-and-announce (Taiwan-countdown-inspired).** Each agent commits to its plan for the next few seconds so neighbours can trust it and countdown timers stay honest.

## 4. All-in-one system modules (the ambitious capstone/product)
| Module | What it does | Status |
|---|---|---|
| **Self-learning hub** | per-junction continual learning, time-aware | **CORE** |
| **Green-wave coordination** | neighbour messages, corridor progression | **CORE** |
| **Ambulance green corridor** | emergency vehicle becomes a high-priority message propagated *ahead*; agents pre-clear a corridor **and learn to un-jam cross-traffic afterward** (improves on GPS/IR preemption like Opticom/BATCS, which override per-signal and leave a mess) | improved add-on |
| **Sensor-failure resilience** | camera dropout / noisy counts → graceful fallback to safe local timing | improved add-on |
| **Fault tolerance** | a dead/offline junction doesn't break neighbours' coordination | improved add-on |
| **Neighbourhood fairness** | prevent side-roads / poorer zones being permanently starved of green | optional |
| **Dashboard + insights** | live view of green waves + metrics; later, flag junctions no timing can fix (road-design signal) | product layer |

## 5. Why this is worth doing
- **Bengaluru already runs BATCS** (169+ junctions → 500+, cameras, C-DAC's **rule-based** CoSiCoSt, corridor green waves, GPS ambulance priority). So the sensing infra exists and the city believes in adaptive signals. Saarathi answers the open question: *can a signal that **learns its own junction** and **keeps improving** beat hand-written rules for Indian mixed traffic?*
- Existing adaptive/MARL work (CoLight, MA2C, PressLight, SCOOT/SCATS/BATCS) is either rule-based or trained-once on Western lane traffic. A **per-junction, continually self-learning, time-aware** controller for lane-less Indian traffic is a genuinely useful and under-explored angle — and honest, real-world impact for Bengaluru.

## 6. How it's evaluated (the proof)
- **Where:** one Bengaluru-style corridor, **3–6 junctions**, OSM geometry, SUMO sublane model (lane-less), traffic in PCU, calibrated to real modal split + counts where available; **state every assumption**.
- **Time realism (the whole point):** run a full day-profile (morning peak → lull → evening peak → night), and multiple days, so the self-learning/time-adaptation is actually exercised — not one flat demand.
- **Baselines:** fixed-time · actuated · **max-pressure (tuned — must beat this)** · a documented **"CoSiCoSt-inspired rule-based proxy"** (honest name, published pseudo-code, fairly tuned — *never claim "we beat BATCS"*) · independent RL (no coordination).
- **Ablations (show what matters):** no continual learning (train-once) · no time context · no neighbour coordination.
- **Metrics:** stops/vehicle (headline) · average delay · travel time · queue/spillback · **improvement-over-days curve** (proof it keeps learning).
- **5+ seeds.**

## 7. The one claim to defend (paper)
> *In a Bengaluru-corridor simulation with mixed lane-less traffic over realistic daily demand, per-junction agents that continually learn each junction's time-varying traffic and coordinate via neighbour messages reduce stops and delay versus fixed-time, actuated, max-pressure, a rule-based adaptive proxy, and non-coordinating RL — and keep improving as demand patterns shift.*

**Venue ladder:** capstone (strong) → Indian ITS / transport workshop → IEEE ITSC workshop/poster (realistic) → main ITSC (stretch). Full T-ITS: not this timeline. The all-in-one system also supports a separate **system/demo paper**.

## 8. Build plan — 6–7 months, 3 people, ₹0
- **Phase 0 (wk 1–2):** SUMO + sumo-rl/RESCO tutorials; read papers 04, 10, 19, 22; pick the corridor (e.g. an ORR / Old Airport Rd stretch); decide PCU factors.
- **Phase 1 (wk 3–8):** corridor in SUMO from OSM; Indian vehicle mix + sublane; build the **daily demand profile**; calibrate; **guide sign-off that it looks Indian.** ← riskiest, do first.
- **Phase 2 (wk 9–12):** baselines running: fixed-time, actuated, tuned max-pressure, CoSiCoSt-inspired proxy (pseudo-code + parameter sweep).
- **Phase 3 (wk 13–20):** the self-learning hub — single junction first (time-aware, continual, PCU state) → prove it beats tuned max-pressure on that junction → then add neighbour coordination across the corridor.
- **Phase 4 (wk 21–24):** add-on modules in priority order: **ambulance corridor** → sensor-dropout resilience → (fairness if time). Full experiment matrix × days × 5 seeds + ablations.
- **Phase 5 (wk 25–28):** dashboard/demo (GUI video of a green wave forming = the demo moment), paper, GitHub release, capstone report.
- **Team:** A = simulation + daily-demand calibration · B = baselines + proxy + ambulance module · C = self-learning agent + coordination. Everyone writes.

## 9. Riskiest-first checkpoints (and fallbacks)
1. **Calibration credibility** — if the corridor isn't believably Indian by wk 8, use a principled synthetic corridor, stated openly.
2. **Max-pressure is embarrassingly strong** — if the hub can't beat it by wk 18, reframe honestly as *"when does per-junction self-learning help vs max-pressure in mixed traffic?"* — still publishable.
3. **Live/continual learning is unsafe in reality** — always the sim-twin-then-deploy loop; never claim live online learning on real signals.
4. **RL convergence pain** → shrink action space to phase-extension only, fewer junctions.

## 10. Pitch lines
- **Capstone:** *"Bengaluru spent crores on adaptive signals that follow fixed rules. Saarathi gives every junction its own brain that learns that junction's traffic and gets smarter every single day — no new roads, just software."*
- **Product:** *"A signal that knows its own corner of the city — what Monday 9 am looks like, what Sunday midnight looks like — and keeps learning."*
