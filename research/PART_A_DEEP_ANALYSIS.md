# Part A — Deep Analysis (state of the benchmark, 2026-11-16)

Scope: Part A only (environment + baselines + Studio). Judged against `RULES.md`. Every number below was recomputed from files in `code/experiments/results/` on 2026-11-16. Literature gaps are in a separate file, `research/PART_A_LIT_GAP_REVIEW.md` (written by a parallel session).

## 1. Verdict

The plumbing is good. The evidence is not paper-ready yet. Three problems block any claim, and each would get flagged in a viva or review:

1. **The simulator does not yet show two-wheeler filtering.** That is the one behaviour that makes it "Indian".
2. **Gridlock is distorting the results.** Up to half of the vehicles never finish, and the runs log teleports and collisions.
3. **The 5-seed rankings are not statistically significant, and the results CSVs contain duplicate rows.**

None of these needs new software. They are measurement and protocol fixes, plus the field data that was already on the critical path.

## 2. What is solid (keep)

| Item | Evidence |
|---|---|
| Manifest-driven scenarios | `corridor.yaml` per area. Behaviour profiles, PCU and safety timings all come from the manifest (RULES §7.1). |
| One harness for every controller | `runner.py`, `--controller module:Class`, safety shell, same metric code. |
| Cheap new areas | `make_area.py` turns any OSM area of 4 km² or less into a runnable scenario. 6 areas exist: corridor4, domlur, hebbal, old_airport_road, silk_board, trinity. |
| Real signal data | BTP cycle lengths for Domlur 155 s, ISRO 193 s and Yamlur 100 s (A-006, `sourced`). |
| Safety metrics reported, not hidden | Collisions, junction collisions, teleports, emergency stops and unfinished vehicles are logged on every row. |
| Honest documentation | `assumptions.md` has status labels, and `RULES.md` has a never-claim list. |

## 3. Findings (ranked by how much they block the paper)

### F1. No two-wheeler seepage. Critical; this breaks the core claim.
The realism check (`_sample_front_row`, `runner.py:160`) says filtering exists when the bike share in the first 8 m at a red light is **greater than** the bike modal share. Measured ratio = front-row share ÷ modal share, averaged over the unique runs:

| Area | Profile, demand | Ratio |
|---|---|---|
| silk_board | active 0.6 / literature 0.6 | **1.01 / 1.01** |
| silk_board | active 0.8 / literature 0.8 | **0.82 / 0.93** |
| domlur | active 0.4 / 0.6 | **0.77 / 0.97** |
| domlur | literature 0.8 | **0.75** |

A ratio of 1.0 or less means bikes are **not** reaching the stop line ahead of other vehicles. Under congestion it is worse: bikes end up behind. RULES §3.4 says that turning on the sublane model is not evidence of realism, and this check shows the realism is not there yet. The 2026 Computer Networks seepage paper reports a 0.906 m seepage gap and 80,553 seepage events, against 132 with SUMO defaults. Our vtypes are still close to the defaults on the parameters that matter (`minGapLat` 0.35–0.6, `lcSublane`, `lcPushy`, `minGap` at the stop line).
**Fix:** tune the bike vType (`minGap` ≈ 0.5, `minGapLat` ≈ 0.3, high `lcSublane`/`lcPushy`, `latAlignment arbitrary`) until the ratio is clearly above 1, for example 1.3 or more. Add the ratio as a PASS/FAIL line in `verify.py`. Then run the `lane_disciplined` profile, which has **not been run at all yet** (only `active` and `literature` appear in the results), so the ablation has a real contrast.

### F2. Gridlock and teleports are inside the measured numbers. Critical.
- Unfinished vehicles ÷ inserted vehicles: **Domlur 8–52%**, **Silk Board 5–39%**.
- Domlur 5-seed means: teleports 17–25 per run, collisions 3–9 per run.
- `delay_s` is the mean `timeLoss` over tripinfo records. With `write-unfinished`, vehicles still en route *are* included, but their delay is **truncated at sim end**, so `delay_s` is a lower bound that under-states gridlock. For example, in Domlur fixed s4, 833 of 3,074 records are unfinished. Only about 10 vehicles per run were never inserted (no record at all), and mean departDelay is about 1 s. So the bias is truncation, not missing vehicles. *(Corrected 2026-11-16. An earlier draft blamed the insertion backlog.)*
- **Fixed in the v6 schema:** `run.py` now also writes `completed_trips`, `insertion_backlog`, `depart_delay_s` and `delay_incl_depart_s` to `results_v6.csv`. Read delay beside completed trips.

RULES §5.7 says that a parameter set which needs collisions or teleports is rejected. Domlur's current numbers fail that rule.
**Fix:** (a) add `departDelay`, or an insertion-backlog penalty, to delay, or report "delay incl. depart delay"; (b) report throughput (completed trips) as the headline beside delay; (c) cut Domlur demand, or fix its unsignalled side-road junctions (A-010), until teleports are near 0 at the reported demand; (d) treat any run with teleports above a declared threshold as a failed run in the table, not as a data point.

### F3. The rankings are not significant. High.
Welch t on the 5-seed summaries:
- Domlur, maxp vs fixed: 152 ± 77 s vs 218 ± 133 s → t ≈ 0.95, **not significant**.
- Silk Board at 0.6, maxp vs fixed: 29.5 ± 7.8 s vs 32.2 ± 4.8 s → t ≈ 0.65, **not significant**. At 0.6 Silk Board is also nearly uncongested: mean waiting is 4–15 s. Every controller looks the same, so the regime cannot tell controllers apart.

So "Max-Pressure wins" is currently a direction, not a result. The memory note of 46.5 s vs 69.4 s comes from synthetic corridor4, which RULES §2.7 counts as a sanity check only.
**Fix:** use 10 or more seeds, use paired comparisons (same seed, same demand file; report the per-seed difference with a 95% CI), and choose a demand level where the controllers separate (a demand sweep of 0.4 / 0.6 / 0.8 / 1.0 per area). This also feeds contribution C3 (stability as an evaluation axis) with real statistics rather than an anecdote.

### F4. Duplicate rows and a fragile summariser. High; this is a reproducibility bug.
- `silk_board/results_v5.csv`: **66 rows, 32 unique** (profile, demand, controller, seed). One key appears 5 times. Domlur has 23 rows and 19 unique.
- `summarize_results.py` takes the last `--last N` rows (default 9). If the CSV has duplicates or runs in a different order, the summary silently averages the wrong runs.

RULES §7.3 says every number must be regenerable from a logged command.
**Fixed 2026-11-16:** `summarize_results.py --input <csv>` keeps the latest row per run key, groups by (scenario, profile, hours, demand, controller), and writes the git SHA and command on line 1. `--last` is gone. Re-summarising confirmed the duplicate counts: Domlur had 4 duplicates and Silk Board 34.

### F5. 45 files uncommitted, including all the 5-seed results and Studio. High.
`git status` shows 45 changes: `studio.py`, `make_area.py`, all OSM scenarios, `data_sources.md`, and every per-area result. RULES §7.5 violation. One bad edit loses the only evidence.
**Fix:** commit now and tag `v5-part-a-studio` (task A1 in `PART_A_COMPLETION.md`). Leave the tripinfo XMLs (about 1.9 MB each) to `.gitignore` or Git LFS. The CSVs are what need to be in git.

### F6. Calibration is at zero. Critical path, already known.
No field counts. Demand is `randomTrips`/`duarouter` scaled from a capacity guess (A-009, A-013, `provisional`). Phase splits are SUMO defaults scaled to the BTP cycle (A-007, `provisional`). A-001 to A-004 are still `pending`/TBD, including **the two-wheeler PCU**, which is the parameter the PCU story depends on.
Usable now without fieldwork:
- **Pune dataset** (Matange & Abraham 2026, CC BY 4.0). Checked in `research/pune_dataset_check/`. It covers a real 3-junction stretch with 192 camera-hours. Good for a *calibration-method demo* and the modal-split prior. Weaknesses: no autos, the directions are on-screen rather than turning movements, and it is not Bengaluru.
- **Indo-HCM saturation flow** for a discharge-rate check.

A Bengaluru field count (2 junctions × 3 windows, with one window held out) is still what makes the work publishable as *Bengaluru-inspired, calibrated*.

### F7. Smaller issues
- The PCU sensitivity check (RULES §3.3) has not been run: no `indo_hcm`/`calibrated` PCU set has been run against `static_irc`.
- External baselines (MPLight/CoLight, task A4) have had neither a spike nor an exclusion note.
- No clean-machine reproduction yet (task A5).
- `requirements.txt` changed but is not pinned with the SUMO version and seed list.

## 4. Readiness score (verified, not planned)

| Part A deliverable | Status |
|---|---|
| Runnable, manifest-driven environment | ✅ done |
| Plug-in controller harness + Studio | ✅ done (not committed) |
| Baselines across 5 seeds | ⚠️ runs exist; stats not significant; duplicates |
| Realism checks (L6) | ❌ 1 of 5 checks built, and it **fails** |
| Lane-disciplined ablation | ❌ not run |
| PCU sensitivity | ❌ not run |
| Field data + calibration/validation | ❌ none |
| External RL baseline decision | ❌ not started |
| Clean-machine reproduce + release | ❌ not started |

Build is about 55%. **Paper-readiness is about 15%**, slightly *lower* than the ~18% estimate from 2026-11-10, because F1–F3 were not known then.

## 5. Order of work (riskiest first, each with a check)

1. **Commit + tag** (F5). Check: clean `git status`.
2. **Fix the metrics and the summariser** (F2a–b, F4). Check: summary refuses duplicate keys; delay includes depart delay.
3. **Tune the bike vType until seepage appears** (F1). Check: front-row ratio ≥ 1.3 on silk_board at 0.6 and 0.8; `lane_disciplined` gives a ratio of about 1.0 or less. *If seepage can't be produced, that is itself a reportable finding about SUMO's sublane model, so log it honestly.*
4. **Remove gridlock at the reported demand** (F2c–d). Check: teleports ≈ 0, unfinished < 5% at the demands in the table.
5. **Demand sweep, 10 seeds, paired stats** (F3). Check: a 95% CI table per area; state where maxp vs fixed separates and where it doesn't.
6. **Calibration-method demo on Pune**, then **Bengaluru field counts** with a held-out window (F6). Check: the GEH gate is reported pass or fail.
7. PCU sensitivity, external-baseline decision, clean-machine reproduce (F7).

Steps 1–5 need no fieldwork and come to roughly one week of focused work. Step 3 matters most, because without it "Indian mixed-traffic benchmark" is only a label.

## 6. How this connects to the literature-gap review

Our own data has already produced two candidate contributions that the gap review should test for novelty:
- **Seed-variance / stability as an evaluation axis**: rankings swing a lot across seeds (Domlur delay SD is 50–60% of the mean).
- **Whether SUMO's stock sublane model reproduces filtering**: F1 is a measurable, reportable question, and only the 2026 seepage paper touches it.

Cross-check them against the gap matrix in `PART_A_LIT_GAP_REVIEW.md` once it lands.
