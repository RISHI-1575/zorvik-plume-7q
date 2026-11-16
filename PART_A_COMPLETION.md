# Part A — Completion Plan & Paper Strategy

**Written 2026-11-11.** Authority: `PROJECT_DEFINITION.md` → `FINAL_PLAN.md` → `RULES.md`. This doc lists what remains for Part A to be **done**, and the strategy that turns the whole project into one publishable system. It adds no scope.

---

## 1. What "Part A done" means (from FINAL_PLAN.md)

| Deliverable | Done when |
|---|---|
| Environment | Another person can clone, run the reference scenario, and get comparable metrics |
| Benchmark | Fixed-time, Max-Pressure (+ feasible MPLight/CoLight adapters) evaluated under identical demand and seeds |

Verified today: manifest-driven scenarios (corridor4 + any OSM area via Studio), fixed/actuated/max-pressure/own-plan + plug-in controller API, 5-seed results on 3 Bengaluru areas, verify.py green, assumptions + data sources documented.

---

## 2. Remaining work (ordered; each item has a hard "done when")

### A1. Version control + hygiene — *first, 1 hour*
- Commit the Studio + 5-seed work; tag `v5-part-a-studio`. (RULES 7.5: commit after every verified milestone — 37 files currently uncommitted.)
- Revoke and remove `openai-api-key.txt` from the parent folder (RULES 7.6).
- **Done when:** clean `git status`, tagged, key revoked.

### A2. Field data collection — *the critical path (RULES 8.2: outranks everything else)*
- Choose ONE corridor (recommendation: Old Airport Road — scenario + BTP cycle data already exist).
- Collect classified turning counts, signal timings, queue lengths in AM-peak / midday / PM-peak windows. Reserve one **held-out** window before any tuning (RULES 4.1–4.2).
- Method per `SIMULATOR_RESEARCH_AND_BUILD_PLAN.md` §6: public observation points, manual/clicker counts, no faces or plates.
- **Done when:** anonymised counts + data dictionary committed under `code/data/field/`, held-out window sealed.

### A3. Calibration + validation against the pre-declared gates
- Tune demand, modal split and vtypes on the tuning windows only; validate on the held-out window.
- Gates (RULES 4.3, declared before tuning): ≥85% of turning flows GEH < 5 · travel-time error ≤ 15% · median queue error ≤ 20% · modal-share error ≤ 5 pp · no reliance on collisions/teleports · visible two-wheeler filtering.
- Anchor against literature: saturation flow and speeds vs Anusha, Verma & Kavitha (ASCE JTE 2013) values.
- **Done when:** calibration table (parameter, source, before/after) + validation report committed; missed gates documented, not hidden.

### A4. External baseline decision (MPLight / CoLight)
- Time-boxed feasibility spike (≤2 days): can they be adapted *fairly* — same network, seeds, safety shell — to a non-lane sublane network?
- RULES 5.4: a lightly-tuned external baseline is worse than omitting it with a stated limitation.
- **Done when:** either a working adapter in the harness, or a written exclusion note in `LITERATURE_AUDIT.md`.

### A5. Clean-machine reproducibility test
- A teammate (not Rishi's machine) clones, follows README, reproduces the 5-seed Silk Board table within noise.
- Pin: `requirements.txt` exact versions + SUMO version + seed list.
- **Done when:** teammate's numbers archived next to the originals.

### A6. Demo polish (small, after A2–A3)
- XQuartz install for "Watch in SUMO" (needs Rishi's admin password): `brew install --cask xquartz`.
- One scripted 3-minute Studio demo path added to `PRESENTATION_READINESS.md`.
- **Done when:** demo runs start-to-finish from the script on the clean machine.

### A7. Release package (closes Part A, per RULES 7.4)
- One-command reproduce guide · manifests + source dates + licences · anonymised counts + dictionary · calibration/validation scripts + results · controller API docs · seeds + environment lock · tagged archive (public repo or institute archive).
- **Done when:** the tagged archive alone is enough to reproduce every reported number.

**Not part of Part A:** PPO training, neighbour messages, ambulance (Part B, parked). More Studio features. City-scale anything.

---

## 3. Making it publishable: one system, one story

### The problem space (the paper's opening, in our words)
Signal-control RL research is benchmarked almost entirely on lane-disciplined, homogeneous traffic (RESCO, CityFlow, standard SUMO grids). Indian junctions violate every assumption: no lane discipline, 6+ vehicle classes, two-wheeler filtering to the stop line, PCU-based capacity. There is **no open, reproducible, field-calibrated benchmark** for this regime — so published controllers are untested where they're needed most. Saarathi closes that gap.

### The cumulative system (each part feeds the next)
1. **The benchmark** — calibrated scenarios + fixed metrics + 5-seed protocol + plug-in API (Part A).
2. **The test bench** — Studio: anyone picks a Bengaluru area and races their controller against the baselines (Part A, the demo + adoption hook).
3. **The reference controller** — safety-shelled decentralised PPO with 3-field interpretable messages + ambulance recovery metric (Part B, evaluated *on* 1–2).

### Contribution stack for the paper (strongest first)
- **C1. The benchmark itself.** Benchmark papers are a recognised genre (RESCO precedent). Ours is the first open one for non-lane heterogeneous traffic with field calibration.
- **C2. Original field data + calibration recipe.** Even modest manual counts are scarce and valuable; the GEH-gated recipe is reusable. This is what reviewers can't get elsewhere.
- **C3. Stability as an evaluation axis.** Our own 2026-11-10 finding: on Domlur, the 1-seed ranking *reverses* across 5 seeds (fixed-time has near-gridlock seeds; max-pressure is stable). Propose reporting variance/worst-seed alongside mean delay. Cheap to add, genuinely useful, born from our data.
- **C4. The safety shell spec** — unsafe switches impossible by construction, identical shell wrapping every learned method (fairness, RULES 5.3).
- **C5. Unseen-area generalisation protocol.** `make_area.py` makes test areas nearly free: tune/train on one corridor, evaluate zero-shot on others. No lane-free benchmark offers this.
- **C6. The Saarathi controller** (Part B) — must beat *tuned* Max-Pressure on unseen seeds before it is a claim at all (RULES 5.5).

### Venue ladder (realistic for a capstone)
1. arXiv preprint + public repo + hosted Studio demo (impact engine; do first).
2. IEEE ITSC / an RL-for-transport workshop (benchmark + early controller results).
3. Transportation Research Part C / IEEE T-ITS (stretch: full system with C2 field data + C6).

### Impact beyond the paper (the "Reddit test")
- Host Studio publicly: **"Upload your algorithm. Beat Silk Board."** — a leaderboard per area, seeds fixed by us.
- The hook is the place-name: everyone in Bengaluru has suffered Silk Board. A tool where *your code* fights *that junction* is shareable in a way a PDF never is.
- Secondary audiences: other Indian cities via OSM (works anywhere), teaching (youth-facing bench), civic-tech communities.

### What we never claim (LITERATURE_AUDIT.md)
First Indian RL/simulator · novel learned communication · novel ambulance recovery · beats BATCS · digital twin · deployment. Safe claim: **reproducible Bengaluru-inspired benchmark + reference controller**.

---

## 4. Market positioning: what Dubai's UTC-UX Fusion teaches us

**What the UAE is building (researched 2026-11-11).** Dubai RTA's **UTC-UX Fusion** (announced Feb 2025, completion H1 2026, all signals AI-managed by early 2027): AI + predictive analytics + a proprietary digital twin — every signal-timing change is simulated and assessed *before* being applied to a real junction. Targets 10–20% journey-time/congestion reduction; priority for emergency vehicles and public transport; future V2X. Separately, ~50 AI traffic monitoring stations on UAE federal highways (Nov 2026).

**The lesson.** Dubai's key component is not the AI — it is the **simulate-before-deploy gate**. That is exactly what Saarathi is, for traffic Dubai's twin cannot model: their system assumes lane discipline, homogeneous vehicles, and a petro-state sensor budget. **Repositioning: Saarathi is the missing pre-deployment evaluation layer for Indian cities** — when a smart-city tender buys an adaptive signal system, there is no open tool to answer "will this work at our junction, with our traffic?" before crores are spent. Studio's own-plan controller already lets a city race any vendor's algorithm against its real signal plan on its own OSM junction. (We say "pre-deployment evaluation layer", never "digital twin" — never-claim list.)

**Add-ons (small tweaks, large uniqueness):**
1. **Sensing-cost axis** *(top pick, genuinely novel)*: run every controller under three sensing tiers — full queue state / stop-line counts (one cheap camera) / 15-min aggregate counts — and report the degradation curve. Trivial in SUMO (mask the observation); no benchmark offers it; it answers a real procurement question for tier-2/3 Indian cities.
2. **Junction report card**: one auto-generated page per Studio run (journey time, delay, worst-seed, safety counts, later ambulance recovery) in the KPI language Dubai uses.
3. **Coordination without V2X**: Part B's 3-field signal-to-signal messages vs Dubai's vehicle-hardware V2X roadmap — *green waves for cities that can't afford V2X*.
4. **Emergency priority is market-validated**: Dubai headlines it; our ambulance + cross-street recovery metric is the twist nobody reports.

### Uniqueness table

| Dimension | Dubai UTC-UX Fusion / UAE | Research benchmarks (RESCO, CityFlow) | BATCS / Indian ATCS deployments | **Saarathi** |
|---|---|---|---|---|
| Traffic model | Lane-disciplined, homogeneous | Lane-disciplined, mostly synthetic | Real Indian traffic, but closed | **Non-lane, 6-class heterogeneous, PCU-based, field-calibrated (A2–A3)** |
| Architecture | Centralised city UTC + control room | Mostly centralised training | Centralised | **Today: independent per-junction controllers + safety shell, no coordination. Decentralised learned agents with neighbour messages = Part B, not built** |
| Sensing assumed | Dense sensors, V2X roadmap | Perfect simulator state | Vendor cameras/loops | **Benchmarked across sensing tiers, down to counts a poor city can afford** |
| Pre-deployment testing | Proprietary digital twin | Not the goal | None public | **Open evaluation layer: anyone tests any controller on any OSM junction (Studio)** |
| Coordination | V2X / C-ITS (vehicle hardware) | Learned latent messages (uninterpretable) | Fixed corridor plans | **Planned (Part B, not built): 3-field interpretable signal-to-signal messages, no vehicle hardware** |
| Emergency handling | Priority (headline feature) | Rarely modelled | Manual green-corridor ops | **Priority + cross-street recovery metric** |
| Cost & openness | Vendor contracts, closed | Open but not India-relevant | Crores, closed | **Open source, laptop-runnable, 5-seed reproducible** |
| Honest claim | "10–20% improvement" (press) | Algorithm leaderboards | Deployment | **Reproducible Bengaluru-inspired benchmark + reference controller — no deployment claim** |

**Elevator pitch:** "Dubai built a digital twin to test signal AI before deploying it. India can't import theirs — the traffic physics is different and the price is impossible. Saarathi is that layer, open source, for Indian roads."

---

## 5. Order of execution

A1 (today) → A2 field counts (needs team, plan the site visit now) → A3 calibrate/validate → A4 + A5 in parallel → A6 → unpark Part B → A7 release ships with the paper draft.
