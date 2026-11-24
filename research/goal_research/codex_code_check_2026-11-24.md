## Recommended goal

**Problem.** On a Bengaluru corridor where two-wheelers filter through queues, would changing how two adjacent signals allocate green actually reduce delay, or does the apparent benefit depend on how the simulator models the bikes?

**Solution.** Build one reproducible, field-checked SUMO comparison on two adjacent Old Airport Road signals. Use Part A to measure filtering and test its influence on controller rankings. Use Part B to test whether a small PPO policy choosing between two pressure rules earns its complexity over tuned PCU max-pressure.

The city-facing deliverable is a decision table showing seconds saved per trip, how many trips finished, and whether the recommendation survives plausible traffic assumptions. This makes a single paper even if classical control wins. Prior work already covers heterogeneous pressure/RL control, Chennai laneless RL, field-calibrated seepage, and learning over pressure controllers. Saarathi’s contribution would be evidence about **which timing choice survives those assumptions on this corridor**. [Agarwal et al. [P]](https://doi.org/10.1016/j.eswa.2024.124416) · [Nandakumar et al. [PP]](https://arxiv.org/abs/2509.21745) · [Guin et al. [P]](https://doi.org/10.1016/j.comnet.2026.112510) · [Com-MP [PP]](https://arxiv.org/abs/2610.31037)

## What the checkout supports today

I inspected source, manifests, saved outputs and Git status. I did not rerun simulations or modify files.

| | Implemented and evidenced | Gap and estimated student-days |
|---|---|---|
| **A · Environment** | Manifest-driven mixed traffic, PCU queues, sublane profiles, same-lane bike-pass counter, Studio and plug-in runner. Four OSM areas have manifests. `corridor4` is synthetic. Hebbal has map assets only. Silk Board has one signal. | Verify two connected Old Airport Road signals, movements and phase order **2–3**. Collect classified turns, timings, queues, corridor times and observable bike passes across three windows, then calibrate and validate **10–14**. |
| **A · Evidence** | Fixed, actuated, network-program and PCU max-pressure implementations exist. Saved runs include trip records, completions, backlog and safety events. The review reports ~3.2× seepage versus the repo’s `literature` profile. Five-seed results do not establish a controller winner. | Regenerate missing v7 summary evidence **1–2**. Diagnose gridlock and add a demand cutoff plus drain period **3–5**. Build paired analysis and PCU sensitivity **3–4**. Pin versions, resolve dirty files and reproduce on a teammate’s laptop **2–3**. [Part A audit](</Users/rishi/Personal/final year project/Saarathi/research/PART_A_DEEP_ANALYSIS.md>) |
| **B · Control** | One PPO checkpoint and a completed evaluation log. PPO controls one four-arm, two-green reference junction, requests phases directly and leaves its neighbours on max-pressure. The shell handles minimum green, yellow and all-red. Maximum green depends on callers checking `must_rotate()`; PPO does not. | Enforce maximum green inside the shell and test actual phase traces **2–3**. Adapt observations, integrate a shared two-choice policy at both junctions and add released-PCU/ETA messages **5–8**. Tune, train and evaluate **5–8**. Ambulance flag, pre-emption and recovery comparison are absent from the controller path; budget **6–9 additional** if retained. [PPO environment](</Users/rishi/Personal/final year project/Saarathi/code/src/saarathi/env.py>) · [Controllers](</Users/rishi/Personal/final year project/Saarathi/code/src/saarathi/controllers.py>) |

## Features, experiments and paper table

**Must-have.** One observed signal pair, versioned assumptions, raw counts, a held-out field window, matched signal clearances, and a one-command table. Give PPO two actions at each junction: serve the highest local pressure, or serve the highest pressure after accounting for an incoming platoon. Test both rules independently so any gain from the message can be distinguished from gain from learning.

**Nice-to-have.** Ambulance priority with cross-street delay and recovery, followed by an unseen-area test. I recommend explicitly revising the existing ambulance commitment. Reserve weeks 7–8 for reproduction and writing.

Freeze validation gates before tuning. Use identical routes, warm-up, demand cutoff and drain limit across controllers. Test two demand levels and ten unseen paired route seeds each. Train PPO with three independent training seeds. Repeat the primary comparison under filtering versus classic lanes, vehicle counts versus PCU, and an alternative PCU set.

| Controller · repeat per demand | Delay including departure wait, s/trip | Paired Δ vs tuned MP, 95% CI | Completed/scheduled | Failed runs/10 | Ranking changes under sensitivity? |
|---|---:|---:|---:|---:|---|
| Observed fixed plan / actuated / tuned local MP / message-aware MP / PPO selector — one row each | Measured | Measured | Measured | Measured | Report which assumption |

## Five risks and fallbacks

1. **Field validation fails.** Publish measured discrepancies and assumption sensitivity. Withhold corridor-specific timing advice.
2. **Gridlock truncates delay.** Count every failed run. If collisions, teleports or an undrained backlog persist, report that regime as a stress test.
3. **PPO ties or loses.** Report the paired interval and retain the simplest competitive rule.
4. **Signal transitions violate the contract.** Replay adversarial hold/switch requests. Restrict evaluation to verified phase sequences.
5. **Laptop runs overrun.** Time a complete paired block in week one. Drop optional areas and ambulance experiments first, preserving held-out seeds and baseline tuning.
