# Saarathi — Project Rules (The Constitution)

**Version:** 1.0 · **Date:** 2026-11-10 · **Applies to:** v6 final scope (2026-11-24)
**Binding order of authority:** `PROJECT_DEFINITION.md` → `FINAL_PLAN.md` → this file → everything else. If any document, slide, commit message, or conversation contradicts these, these win. Archived docs (`IDEA.md`, `IMPLEMENTATION.md`, old README sections) define **nothing**.

This file exists so that no team member, mentor conversation, demo, AI assistant, or late-night enthusiasm can quietly re-expand, re-brand, or overclaim the project. Every rule below traces to the literature audit, the simulator research plan, or a verified gap in the current code.

---

## 1. What the project IS (the two-part commitment)

**Part A — the environment.** An open, reproducible, configurable SUMO benchmark for Indian mixed, weak-lane-discipline traffic: Bengaluru-inspired corridor, six vehicle classes, sublane filtering, PCU-based sensing, documented assumptions, seeds, and a one-command reproduce path.

**Part B — the controller.** Saarathi: a safe, decentralised, PCU-aware reference controller. One PPO agent per junction behind a hard safety shell; explicit neighbour messages limited to `released PCU · ETA · emergency flag`; green-wave coordination; ambulance priority with a cross-street recovery metric.

**The project is complete when, and only when,** another person can clone it, rebuild the reference corridor, run fixed-time / actuated / Max-Pressure / Saarathi under identical demand and seeds, and reproduce the published table.

Anything else — nightly retraining, fairness optimisation, sensor-failure modules, dashboards, city scale — is **optional, and forbidden to start** until both parts above are done and verified.

---

## 2. Claims rules (non-negotiable)

These come straight from `LITERATURE_AUDIT.md`. Violating any of them in a paper, slide, report, or viva answer is the fastest way to be rejected or embarrassed.

**NEVER claim:**
1. "First RL for Indian traffic" / "first open Indian environment" — SiMTraM, Savithramma & Sumathi (2023), Agarwal et al. (2024) and others exist.
2. "Novel learned communication / GAT communication" — CoLight and Bokade et al. already did it.
3. "Novel ambulance recovery" — Qin & Khan (2012), Kiani & Saraç (2023), EMVLight exist.
   - Also never claim a "novel safety shell" — Com-MP (arXiv 2610.31037, preprint) already does safe RL over max-pressure.
4. "Beats BATCS" — unless the actual BATCS software is run under a disclosed fair protocol (it won't be). The honest phrase is "a rule-based adaptive proxy," if one is ever built.
5. "Digital twin of Bengaluru" — it is a Bengaluru-*inspired* scenario.
6. Real-world deployment, live online learning on real signals, or congestion solved.
7. Any paper-grade performance claim from the **synthetic** corridor. Synthetic results are engineering sanity checks only.

**ALWAYS claim (the one defensible line):**
> We release a reproducible, Bengaluru-inspired SUMO benchmark that makes Indian heterogeneous, weak-lane-discipline traffic assumptions explicit, and use it to compare traffic-signal controllers under a common protocol.

Saarathi's controller is the **reference method and demonstration**, not the paper's algorithmic novelty. The novelty is the benchmark + protocol + evidence.

**Paper citation rule:** a paper may be cited as published only after its final venue is verified. Everything else is labelled *preprint*. The `papers/` folder (22 PDFs) is a historical collection, not a vetted bibliography; the vetted list is in `LITERATURE_AUDIT.md` §"Published core literature to cite" (15 entries: SUMO, CityFlow, RESCO, LibSignal, MA2C, PressLight, CoLight, Bokade, CVLight, Savithramma & Sumathi, Agarwal, Padinjarapat & Mathew, Qin & Khan, EMVLight, Kiani & Saraç).

---

## 3. Assumption rules

1. **Every simulator value used in a paper result must have a row in `docs/assumptions.md`** with source, uncertainty, and a validation status (`provisional → sourced → measured → calibrated → validated`, or `rejected`).
2. No parameter may be called "Indian" or "Bengaluru" because it looks plausible. It must be sourced, measured, calibrated, or explicitly labelled provisional.
3. **PCU is never a universal constant.** IRC 106:1990 itself makes factors composition-dependent. The scenario manifest must always carry versioned factor sets (`static_irc` baseline + `calibrated` when field data exists), raw class counts must be kept beside every PCU aggregate, and a PCU sensitivity check is part of the results.
4. Enabling SUMO's sublane model is **not** evidence of Indian realism. Realism is demonstrated only by behavioural checks: two-wheeler seepage to the stop line, staggered queues, discharge rates, class-specific gaps — compared against field evidence.

---

## 4. Calibration and validation gates

No controller-performance claim is paper-ready until the simulator passes independent validation.

1. Field data comes first: classified turning counts, signal timings, and queues at the chosen corridor, in AM-peak / midday / PM-peak windows, with one **held-out** period reserved before any tuning.
2. **Calibration and validation must use different data.** Reporting fit on the tuning data as "validated" is forbidden.
3. Acceptance gates are declared **before** tuning (starting values, revisable only before controller evaluation): ≥85% of turning flows with GEH < 5 · corridor travel-time error ≤ 15% · median queue error ≤ 20% · modal-share error ≤ 5 pp · no result may depend on collisions/teleports · visible two-wheeler filtering.
4. A missed gate is documented, never hidden. Gates may not be revised after seeing controller results.
5. Field work follows the safety/privacy rules in `SIMULATOR_RESEARCH_AND_BUILD_PLAN.md` §6: public observation points only, no faces or licence plates stored, permission obtained before any video recording.

---

## 5. Experiment fairness rules

1. Every controller gets **identical** network, routes, seed set, warm-up, evaluation window, metric code, and safety constraints. One harness runs them all.
2. **Minimum 5 seeds** for any reported comparison; report mean + SD or 95% CI, and archive raw per-seed outputs (CSV + tripinfo) with the exact command.
3. The same safety shell wraps **every** learned method, including external baselines. Comparing shelled Saarathi against unshelled baselines (or vice versa) is unfair and forbidden.
4. External RL baselines (MPLight/CoLight/etc.) are added **only** if they can be adapted fairly to this SUMO network. A broken or lightly-tuned external baseline is worse than omitting it and stating the limitation.
5. Max-Pressure must be **tuned**, not strawmanned. It is currently the strongest controller; Saarathi's PPO must beat tuned PCU Max-Pressure on unseen seeds before any coordination work counts as a result.
6. Required ablations (they ARE the paper's evidence): lane-disciplined vs sublane · vehicle-count vs PCU state · independent vs message-coordinated PPO · (ambulance scenario) no-priority vs conventional pre-emption vs Saarathi priority.
7. Metrics are fixed: completed trips/throughput, delay, travel time, waiting, stops/vehicle, queue/spillback, per-class delay, corridor journey time, collisions, teleports, emergency-braking, ambulance travel time + cross-street recovery time, runtime. Collisions and teleports are **reported, never suppressed** — a parameter set that needs them is rejected.

---

## 6. Safety rules (the controller contract)

1. A junction agent may only **request** a phase. The non-learned safety shell enforces min green (10 s), max green (60 s), yellow (3 s), all-red (2 s) — values owned by the scenario manifest, not code constants.
2. An unsafe switch must be impossible regardless of what the policy learns. The shell is engineering, not a research claim.
3. All learning happens **in simulation only**. No claim or implication of learning on live road users, ever.
4. Neighbour messages are exactly three fields: released PCU, ETA, emergency flag. Adding message content requires a scope decision recorded in `VERSION_HISTORY.md` — it directly trades away the "interpretable explicit messages" positioning.

---

## 7. Code and reproducibility rules

1. **The manifest is the single source of truth.** Junction count, vehicle classes, modal split, PCU sets, safety timings, demand profiles live in `scenarios/<name>/corridor.yaml` and nowhere else. A duplicated constant (e.g. a second `N_JUNCTIONS`) is a bug.
2. `verify.py` (rebuild + 5 contract tests + clean smoke run) must pass before any result is shared or any demo is given.
3. Every results file in `experiments/results/` must be regenerable from a logged command + seed. Untraceable numbers do not exist.
4. The release package (Phase 7) ships: install + one-command reproduce guide, manifest + source dates + licences, anonymised counts + data dictionary, calibration/validation scripts and results, controller API + baselines, seeds + environment lock, and a tagged archive.
5. **Put `code/` under git immediately.** It is currently not version-controlled; one bad edit can silently destroy verified work. Commit after every verified milestone. (As of 2026-11-10 only `showcase/` has a repo.)
6. Secrets never live in the project tree. (`openai-api-key.txt` currently sits in the parent folder in plain text — revoke/move it.)

---

## 8. Process and scope rules

1. **Build order is fixed** (from `FINAL_PLAN.md`): ① finalise + document environment → ② reproducible runner + fixed/actuated/Max-Pressure across seeds → ③ PPO on one junction, beat tuned Max-Pressure → ④ neighbour messaging vs independent → ⑤ ambulance + recovery metric → ⑥ external baselines + release. Skipping ahead (e.g. coordination before the one-junction PPO gate) is forbidden.
2. **The calibration gate outranks AI features.** Per `PROJECT_STATUS_AND_PUBLICATION_PLAN.md`: field counts and the calibration table come before any further learning features. "More RL" never substitutes for "credible environment."
3. Scope changes require a new row in `VERSION_HISTORY.md` with date and reason. A scope change that exists only in chat or in someone's head did not happen.
4. Progress claims use verified percentages (what runs and is checked), never planned-work percentages.
5. Presentation discipline: demo exactly what `PRESENTATION_READINESS.md` scripts; say "synthetic reference prototype," "configurable, four nodes are an instance not a limit," "PCU versioned, to be field-calibrated"; never present the smoke-run PPO model as trained.
6. Any AI assistant (Claude, Codex, GPT) working on this project is bound by this file. Instruct it to read `PROJECT_DEFINITION.md`, `FINAL_PLAN.md`, and `RULES.md` before touching anything, and to leave the archived docs alone.

---

## 9. Standing risk register (watch these)

| Risk | Trigger to act | Response |
|---|---|---|
| Tuned Max-Pressure is too strong | PPO can't beat it after honest tuning | Reframe honestly: "when does learning help vs Max-Pressure in mixed traffic?" — still publishable; never weaken the baseline |
| Calibration not credible | Field gates missed | Document openly, label corridor synthetic-informed; do not quietly claim realism |
| PPO instability | No convergence on one junction | Shrink action space (phase-extend only), longer decision interval, smaller state — in that order |
| Scope creep | Anyone proposes a module not in §1 | Point at this file; log the idea as optional-after-core in `VERSION_HISTORY.md` |
| Overclaiming in viva/paper | Any phrase from §2's NEVER list | Replace with the safe wording table in `LITERATURE_AUDIT.md` |

---

*Change rule for this file: edits require team agreement and a dated note below.*

**Changelog:** 1.0 (2026-11-10) — initial consolidation from PROJECT_DEFINITION v5, FINAL_PLAN v5, LITERATURE_AUDIT, SIMULATOR_RESEARCH_AND_BUILD_PLAN v1.0, PROJECT_STATUS_AND_PUBLICATION_PLAN, PRESENTATION_READINESS, docs/assumptions.md, and a code audit of `code/` (post part-one completion).*
