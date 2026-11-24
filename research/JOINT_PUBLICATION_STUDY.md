# Which field measurements change the choice of traffic-signal controller?

Saarathi joint publication study · 24 November 2026 · Proposed experiment

## Decision and audience

A traffic engineer has counts, signal timings, and a budget for one additional observation. Would measuring when groups of vehicles reach the next signal change which coordination policy the engineer selects? This is an experimentally answerable question about the value of collecting data. The result is useful even if a tuned conventional plan wins. The intended audience is transportation researchers evaluating simulation-based signal decisions.

## Published evidence and its bearing on the claim

| Study | Finding or design relevant here | Consequence for the experiment |
|---|---|---|
| EquiFlow, GIJET, June 2026, Grenze ID 01.GIJET.12.2.321_26, pp. 6018–6026, Tables I–II and §VI | Four Hyderabad junctions, mixed traffic, emergency priority and PPO already occur together. On one held-out realization fixed-time scored above the two evaluated PPO variants. The authors report a defective pedestrian path and different transition handling for Max-Pressure. | Replicate the comparison under matched transitions and several independent demand realizations. Evaluate individual physical outcomes. |
| [Agarwal et al., Expert Systems with Applications](https://www.sciencedirect.com/science/article/pii/S095741742401282X) | Pressure control and RL already address heterogeneous traffic. Publisher summary inspected. | Tune PCU Max-Pressure as a serious competitor. |
| [Indian field study of platoon dispersion](https://www.sciencedirect.com/science/article/pii/S1877042813045266) | Chennai arterial measurements yielded different calibrated dispersion parameters from those in earlier work. | Measure the local downstream arrival distribution. |
| [Recurrence Theory–Based Platoon Analysis](https://ascelibrary.org/doi/10.1061/JTEPBS.0000165) | Published analysis of grouping in Indian laneless arterial traffic. | Vehicle grouping itself is established prior art. |
| [New Approach for Calibrating Robertson’s Platoon Dispersion Model](https://ascelibrary.org/doi/10.1061/JTEPBS.0000141) | Downstream arrival span has already been used for calibration. | Include a conventional dispersion predictor. The added question is whether better predictions change a control decision. |
| [Gandhinagar field-calibrated coordination study](https://www.injoere.com/index.php/injoere/article/view/1865) | The publication record describes field-calibrated network coordination and PCU demand in India. | Compare with a conventional coordinated-offset plan. |
| [RESCO, NeurIPS](https://people.engr.tamu.edu/guni/papers/NeurIPS-signals.pdf) | Reusable benchmark problems and implementations already exist. | Release the field-to-decision evaluation as the reproducible contribution. |
| [Applied Sciences distributed MPC and RL comparison](https://doi.org/10.3390/app16199713) | The comparison controls network, signals and interval and reports differences across demand levels. | Demand-sensitive rankings alone are insufficient evidence for a calibration effect. Cross demand and calibration independently. |
| [Guarded RL evidence audit](https://www.mdpi.com/2076-3417/16/20/10231) | The published audit examines baseline strength, sample size and generalization limits. | Disclose baseline tuning budgets and actual performance against the incumbent. |
| [Incident robustness benchmark](https://link.springer.com/article/10.1186/s12544-026-00841-1) | Published comparative robustness work includes Max-Pressure and multiple networks. | Routine incident stress testing adds little to the central question. |
| [EMVLight, AAAI](https://cdn.aaai.org/ojs/20383/20383-13-24396-1-2-20220628.pdf) | Emergency routing and network signals jointly optimize emergency and ordinary travel. | If included, fix the route and identify which interrupted approaches bear the recovery cost. |

This is a targeted overlap audit. Records, excerpts and previously inspected full-text sections have different evidentiary depth. These studies constrain novelty claims but do not establish priority over the entire literature. ArXiv-only records are excluded from the evidence table.

## Field design

Select a signal pair on Old Airport Road only after verifying that departures can be observed upstream and arrivals can be counted downstream before queues obscure them. Synchronize clocks and log phase changes, departures, turning traffic and major mid-link entries and exits. Keep bikes, autos, cars and heavy vehicles separate. Record missing intervals and occlusion. Double-code a sample to estimate timing and class-count disagreement. An arrival at a standing queue and a departure from the downstream stop line measure different events. Document the detector location and operational definition in both field and SUMO data.

Collect repeated day/time blocks. Lock the split by day before tuning. Use training blocks to fit demand and candidate behaviour settings. On separate selection blocks, select an aggregate-fit set using counts, queues and the project's existing validation gates. From that same set select the settings that also fit within-cycle downstream arrivals under observed signals. Reserve untouched days for the final predictive check. Keep each ensemble's size and selection rule visible. If feasible, compare against randomly narrowed aggregate-fit sets of the same size to detect a benefit caused merely by discarding candidates.

## Controller comparison

Freeze controller weights and tuning before crossing the two calibration sets. Give fixed-time, tuned coordinated offsets, actuated, PCU Max-Pressure, independent PPO and communicating PPO identical route files, signal clearances, phase options and evaluation horizons. Tune baselines using only training data. Distinguish training seeds, demand seeds and independent field days. For each held-out demand, run the same policy in every admissible setting. Keep the external comparator and the paired local-versus-communicating PPO comparison separate.

Compare three inputs to the same learned architecture: local observations alone, upstream released PCU and mean ETA, and estimated arrivals in short time bins. Build the binned forecast only from information available before the decision. Treat perfect future arrivals as an explicitly labelled upper bound if used. Score forecasts at equal lead time and across traffic mixes. Add a time-shuffled upstream-message control to test whether the timing content explains any gain.

## Primary outcome and interpretation

Predeclare the primary policy contrast, a minimum operationally meaningful difference in seconds per demanded trip, and a fixed demand horizon with a drain period. Report cumulative system delay for all demand, insertion backlog, residual vehicles and completions together. If the drain limit leaves vehicles unserved, report their accrued delay and censoring explicitly. Pair policy differences within each demand realization. Quantify uncertainty across days and training runs separately. Choose replication from pilot variability and desired interval width. Hundreds of cycles on one observed day do not supply hundreds of independent days.

For each calibration protocol, name the policy it would select and show the estimated extra delay from choosing it across the behaviour settings supported by held-out observations. Call the quantity simulation-estimated decision loss. Observations under the existing signal plan validate arrival predictions but cannot directly identify real-world outcomes under an untried policy. Report meaningful reversals, ties within the practical margin, or unresolved differences. A narrow stable result is informative. A wide interval is inconclusive. If the richer calibration does not predict held-out arrivals better, the claim that it provides greater fidelity fails.

## Figures and submission evidence

1. Plot synchronized field departure and downstream arrival profiles by class, with the two calibration ensembles and one held-out period.
2. Plot the paired controller delay difference for each accepted parameter set, marking the practical equivalence interval and failed runs.
3. Plot forecast error and the coordination benefit across observed levels of platoon spread. This connects simulator behaviour to a controller action.
4. For an optional ambulance experiment, plot seconds saved against excess cross-street queue-seconds, worst approach delay and the share unrecovered by the end of observation.

The November project audit records a direct same-lane two-wheeler passing metric and a working lane-model ablation. At Silk Board under fixed-time and demand 0.8, it reports rates of 0.0230 for the filtering profile and 0.0070 for the literature profile. That is simulation sensitivity. Local field validation remains outstanding. Domlur's filtering example averaged 17.6 teleports and 9.2 collisions, and unfinished trips truncate reported delay. Diagnose invalid runs, disclose failures by policy and preserve severe valid congestion. Never choose a demand level because it produces a preferred winner.

Before writing a results abstract, archive timestamped aggregate observations, the split, calibration tolerances, frozen controllers, unique run keys, failure logs and a script that regenerates the principal figure. The first submission-worthy milestone is a validated adjacent signal pair and a reproducible estimate of the decision consequence. A second corridor would strengthen external validity. If field observations remain unavailable, report a simulation sensitivity study with explicitly assumed behaviour ranges.
