# Saarathi — Archived Implementation Design (v4-era, 2026-07-10)

> **ARCHIVED — not the active build scope.** This is a detailed earlier design for the self-learning-hub vision. Follow [FINAL_PLAN.md](FINAL_PLAN.md) and [PROJECT_DEFINITION.md](PROJECT_DEFINITION.md) for current work; use this document only as a source of optional implementation ideas.

*Companion to [IDEA.md](IDEA.md) (the what & why). This is the HOW: what to build, in what order, with what tools, and what to focus on at every step. Written for 3 undergrads, 6–7 months, ₹0 budget.*

---

## 0. Final review — additions locked into the design

Going through the idea one last time, these upgrades are now part of the plan (each is low-cost, high-value):

1. **Warm-start, don't learn from zero.** The agent first *imitates* the existing signal plan (fixed-time/actuated) so day-1 performance is never worse than today, then RL improves from there. Kills RL's worst failure mode (garbage early policy) and makes the "self-learning" story deployable.
2. **Hard safety shell around the agent.** The RL agent can only *request* timings; a non-learning wrapper enforces: min green 7s, max green 90s, fixed yellow 3s + all-red 2s, no phase skipped beyond a max wait. Signals can never do something unsafe no matter what the agent learns. (Reviewers and guides both love this.)
3. **PCU-based sensing (Indian Roads Congress values).** One mixed flow, no bike/car discrimination: 2-wheeler 0.5, car 1.0, auto 1.2, bus/truck 3.0. State and rewards all in PCU.
4. **Time-context input.** Time-of-day (sin/cos encoded) + weekday/weekend flag go into the agent's state — this is what makes it learn the junction's *rhythm*, not just react.
5. **Nightly-retrain loop = the "self-learning every day" mechanism.** Day's traffic is logged → appended to a rolling window (e.g. last 30 days) → agent retrains overnight in the digital twin → validated (must beat yesterday's policy on the twin) → only then deployed. Includes a **drift alarm**: if today's traffic differs a lot from the learned pattern (new construction, event), flag for a bigger retrain.
6. **Improvement-over-days curve as a headline result.** Nobody's demo shows a signal getting measurably better each day — ours will. This chart is the emotional core of the paper AND the capstone demo.
7. **Ambulance corridor rides the same message fabric.** Emergency vehicle = one high-priority message propagated ahead along its route; junctions pre-clear; after it passes, agents actively recover the cross-street queues. No separate subsystem to build.
8. **Every module degrades gracefully.** Camera feed dies → junction falls back to its learned time-of-day plan (better than fixed-time even blind) → worst case, plain actuated. A neighbour goes silent → coordinate with whoever's left.

---

## 1. What we are building (system map)

```
                        ┌────────────────────────────┐
                        │        DASHBOARD           │  Phase 6
                        │  live map · metrics · demo │
                        └────────────▲───────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                    CORRIDOR LAYER                       │
        │  neighbour messages (PCU platoon, ETA) · green waves    │  Phase 4
        │  ambulance priority message · fault tolerance           │  Phase 5
        └───────▲──────────────▲──────────────▲───────────────────┘
                │              │              │
        ┌───────┴──────┐ ┌─────┴────────┐ ┌───┴──────────┐
        │  HUB agent   │ │  HUB agent   │ │  HUB agent   │          Phase 3
        │  (junction 1)│ │  (junction 2)│ │  (junction n)│
        │  RL policy   │ │  time-aware  │ │  continual   │
        │  + safety    │ │  + PCU state │ │  nightly     │
        │    shell     │ │              │ │  retrain     │
        └───────▲──────┘ └──────▲───────┘ └──────▲───────┘
                │               │                │
        ┌───────┴───────────────┴────────────────┴───────┐
        │            DIGITAL TWIN (SUMO)                 │            Phase 1
        │  Bengaluru corridor · lane-less sublane ·      │
        │  Indian vehicle mix · daily demand profiles    │
        │  + BASELINES: fixed/actuated/max-pressure/     │            Phase 2
        │    CoSiCoSt-style proxy                        │
        └────────────────────────────────────────────────┘
```

## 2. Tech stack (all free)

| Piece | Choice | Why |
|---|---|---|
| Simulator | **SUMO** (+ sublane model, TraCI API) | standard, models lane-less via sublane |
| Env wrapper | **sumo-rl** (Gymnasium-compatible), customized | saves weeks; already multi-junction |
| RL library | **Stable-Baselines3 (PPO or DQN)** | simplest solid choice for undergrads; RLlib only if scaling pain |
| Language | Python 3.11+ | everything above is Python |
| Maps | OpenStreetMap → `osmWebWizard.py` / `netconvert` | real Bengaluru geometry in minutes |
| Training compute | laptops + **Google Colab** free tier | 3–6 junctions is small-scale |
| Dashboard | SUMO-GUI for demo + **Streamlit** page for metrics | fast to build, looks good |
| Repo | GitHub, one repo, `src/ scenarios/ experiments/ docs/` | code release required for the paper |

## 3. Phase-by-phase plan

### Phase 0 — Setup & literacy (weeks 1–2)
**Build:** dev environments; run SUMO's TraCI tutorial; run one sumo-rl example end-to-end; skim papers 04, 10, 19, 22 in `papers/`.
**Decisions to lock:** corridor choice (pick a 3–6 junction stretch you personally know — e.g. Old Airport Rd or a CBD arterial); PCU values (IRC); phase structures per junction (copy what the real junctions do).
**Focus:** everyone must be able to run a simulation and read/modify a TraCI script. Nothing else matters these two weeks.
**Done when:** `python run_demo.py` shows a junction being controlled by your code.

### Phase 1 — Digital twin (weeks 3–8) ← RISKIEST, HENCE FIRST
**Build:**
1. OSM → SUMO network of the corridor (`osmWebWizard`, then hand-clean junctions/phases in netedit).
2. Indian vehicle types: motorcycle (0.5 PCU, small, nimble), auto (1.2), car (1.0), bus/truck (3.0) with realistic sizes/accel; **sublane model on** (`--lateral-resolution 0.4`) so bikes filter to the front — verify visually that reds grow a bike-carpet up front like real Bengaluru.
3. **Daily demand profiles**: 24h weekday + weekend curves (morning peak ~2×, midday lull, evening peak, night trickle), modal split ~45% 2W / 20% car / 15% auto / 10% bus-truck / 10% other. Source from published Bengaluru stats where possible; otherwise estimate and **write every assumption in `docs/assumptions.md`**.
4. Sensor model: per-approach PCU counts as a real camera would give (aggregate counts, NOT per-vehicle identity) + a noise/dropout switch for later.
**Focus:** believability > precision. The question a guide/reviewer asks is "does this look like Indian traffic?" — bikes swarming to the front, ragged platoons, mixed speeds.
**Done when:** guide watches the GUI and signs off; volumes at peak match your stated sources ±20%.
**Fallback:** if OSM geometry fights you past week 6, build a clean synthetic 4-junction corridor with the same demand realism and say so openly.

### Phase 2 — Baselines (weeks 9–12)
**Build (in this order):**
1. **Fixed-time** — the corridor's current-style plan (SUMO default tlLogic).
2. **Actuated** — SUMO's built-in gap-based actuation, tuned.
3. **Max-pressure** — ~100 lines of Python over TraCI; **tune it properly** (this is the baseline that kills weak papers — ours must be strong and fair).
4. **CoSiCoSt-inspired rule-based proxy** (BATCS stand-in): vehicle-actuated with cycle/split adaptation per documented public descriptions; publish its pseudo-code in `docs/`; parameter-sweep it fairly. **Name it "rule-based adaptive proxy" everywhere — never claim it IS BATCS.**
5. **Metrics harness** (this phase's real product): one command runs any controller × any scenario × N seeds → CSV → plots. Metrics: stops/vehicle, mean delay, travel time, max queue, spillback count, per-time-of-day breakdowns.
**Focus:** the experiment pipeline. From here on, every result comes from `run_experiment.py`, reproducible, seeds logged.
**Done when:** a results table of 4 baselines × weekday profile × 5 seeds exists and max-pressure beats fixed-time (sanity check).

### Phase 3 — The self-learning hub (weeks 13–20) ← THE HEART
**Build, strictly in this order (single junction first!):**
1. **Gym env for ONE junction.**
   - *State:* PCU queue + arrival rate per approach, current phase, time in phase, **time-of-day (sin/cos), weekday flag**.
   - *Action:* keep current phase or switch to next (decision every 5s). Simple beats clever.
   - *Reward:* −(queue PCU) − 0.5·(stops this step) [tune weights once, then freeze].
2. **Safety shell** (wrapper, not learned): min/max green, yellow + all-red insertion, max-wait override. Agent's action passes through this always.
3. **Warm start:** behaviour-clone the actuated controller (~1 day of its decisions) before PPO fine-tuning.
4. **Train PPO on the weekday profile** → must beat tuned max-pressure on that junction. **This is the project's go/no-go gate (week 17).**
5. **Continual-learning loop:** script the day cycle — simulate "today" (sampled variation of the profile) → log → append to rolling window → retrain overnight → validate on twin (deploy only if ≥ yesterday's policy) → next day. Produce the **improvement-over-days curve**.
6. **Drift test:** on day k, permanently change demand (e.g. +40% on one approach = "new mall") → show the nightly loop adapts within a few days while a train-once agent stays degraded. **This chart is the self-learning proof.**
7. Clone to all corridor junctions (each hub trains on its own junction — no shared brain).
**Focus:** ONE junction until it clearly wins. Do not touch multi-junction before the gate passes.
**Fallbacks:** PPO unstable → DQN with phase-extension-only actions; still stuck → longer decision interval (10s), smaller state.

### Phase 4 — Coordination & green waves (weeks 21–23)
**Build:**
1. **Platoon message:** when a phase releases traffic toward neighbour B, send `(PCU released, ETA at B)` (ETA = distance / measured mean speed). Message goes into B's state vector.
2. Retrain hubs with messages on → corridor green waves emerge; verify in GUI (follow one vehicle through 4+ greens — **record this clip, it's the demo**).
3. **Ablations:** coordination off vs on; time-context off vs on; continual off vs on. These three switches ARE the paper's evidence.
**Done when:** corridor stops/vehicle drops visibly vs independent hubs (target ≥10–15%).

### Phase 5 — Add-on modules (weeks 24–26, priority order, cut from the bottom if late)
1. **Ambulance corridor:** ambulance spawns with a route → high-priority message runs ahead → each hub pre-clears (through the safety shell) → after passage, reward temporarily weights cross-street queue recovery. Metric: ambulance travel time vs baselines + recovery time of cross-traffic. *(Improves on Opticom/BATCS-style per-signal preemption: coordinated ahead-of-vehicle clearing + learned aftermath recovery.)*
2. **Sensor resilience:** flip the Phase-1 noise/dropout switch → blind hub falls back to its learned time-of-day plan → show graceful degradation vs rule-based proxy under the same dropout.
3. **Fault tolerance:** kill one hub (stuck plan) → neighbours keep coordinating around it; measure corridor damage vs no-failure.
4. *(only if time)* Fairness metric: report max side-road wait; add a starvation penalty if ugly.

### Phase 6 — Ship it (weeks 27–30)
1. **Demo:** SUMO-GUI side-by-side (fixed-time vs Saarathi, same seed) + green-wave clip + improvement-over-days chart + Streamlit metrics page.
2. **Paper** (workshop, 6–8 pages): gap → twin → hub → coordination → results table → ablations → honest limits (simulation-only, proxy-not-BATCS). Target: IEEE ITSC workshop/poster or Indian transport venue (TPMDC/CTRG); stretch = main ITSC.
3. **Capstone report** = paper + system chapters (modules, dashboard, engineering).
4. **GitHub release:** code + scenarios + `reproduce.md` (required for benchmark credibility).

## 4. Team split (3 people, own your lane, everyone writes)

| | Owner of | Phases they lead |
|---|---|---|
| **A** | Digital twin: network, vehicle types, demand profiles, calibration, sensor model | 1, then supports all |
| **B** | Baselines + rule-based proxy + experiment/metrics harness + ambulance module | 2, 5 |
| **C** | Hub agent: env, safety shell, PPO, continual loop, coordination messages | 3, 4 |

Weekly cadence: Monday 30-min sync (demo what ran, name the blocker); everything in the repo, nothing on laptops only.

## 5. What to focus on (and what NOT to do)

**Focus:**
- The **twin's believability** (Phase 1) and the **max-pressure gate** (Phase 3.4) — the two places the project lives or dies.
- The **three ablation switches** (time-context / continual / coordination) — they are the scientific contribution.
- The **improvement-over-days curve** — the single most persuasive artifact for paper, demo, and viva.
- Reproducibility: seeds logged, one-command experiments, assumptions documented.

**Do NOT:**
- Do not model >6 junctions, city-scale maps, or pedestrians-as-agents.
- Do not invent new RL algorithms or neural architectures — PPO + good state design wins here.
- Do not classify vehicle types at "deployment" — PCU counts only (matches your no-discrimination principle AND what cameras reliably give).
- Do not claim: "beats BATCS", "ready to deploy", "learns live on real signals" — claim the simulation results and the sim-twin-then-deploy pathway.
- Do not chase CoLight reproduction if it eats >2 weeks — the paper's claim doesn't depend on it.
- Do not start the paper in week 27 — B maintains the results table from Phase 2 onward; C keeps a running `docs/paper-notes.md`.

## 6. Milestones at a glance

| Week | Gate | Proof |
|---|---|---|
| 2 | tools run | controlled junction via TraCI |
| 8 | twin believable | guide sign-off + volumes match sources |
| 12 | pipeline + strong baselines | 4-baseline results table, 5 seeds |
| **17** | **hub beats tuned max-pressure (1 junction)** | **go/no-go — metrics table** |
| 20 | self-learning proven | improvement-over-days + drift-adaptation charts |
| 23 | green waves | corridor table + GUI clip |
| 26 | ambulance + resilience | module metrics |
| 30 | shipped | paper draft + demo + GitHub release |
