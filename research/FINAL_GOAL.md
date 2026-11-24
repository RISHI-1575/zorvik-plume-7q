# Saarathi — FINAL GOAL (locked 2026-11-24)

How this was made: a review of the code by Codex, plus three Claude research agents covering real-world evidence, the newest papers (2025–26) and venues/data/compute. The Gemini CLI could not run (Google no longer supports the client) and there was no Perplexity tool, so web search covered both. Raw reports are in `research/goal_research/`.
This file replaces `IMPROVEMENT_PLAN.md` as the working goal. `PROJECT_DEFINITION.md` and `FINAL_PLAN.md` still rule until they are updated to match this file.

---

## 1. The real problem (in plain words)

1. **Indian cities buy "smart" signals, but nobody can check whether they work.**
   - Bengaluru's BATCS covers 169 junctions ([Indian Infrastructure, 2026](https://indianinfrastructure.com/2026/04/06/smart-mobility-a-case-study-of-the-bengaluru-adaptive-traffic-control-system/)). Its claims are "up to 25%", "33%" and "15–20%" less travel time ([DH 2024](https://www.deccanherald.com/india/karnataka/bengaluru/ai-powered-signals-in-bengaluru-reduce-travel-time-by-33-3226394), [DH 2025](https://www.deccanherald.com/amp/story/opinion/how-bengaluru-rewired-its-traffic-signals-to-beat-gridlock-3832080)). None of them gives a baseline, a method or the raw data.
   - No independent audit or open dataset was found.
2. **The standard tests assume traffic stays in lanes. Indian traffic does not.**
   - About 70% of Bengaluru's vehicles are two-wheelers ([OneIndia 2026](https://www.oneindia.com/bengaluru/bengaluru-traffic-1-400-two-wheelers-added-daily-as-bikes-fill-gaps-left-by-public-transport-8065819.html)), and they squeeze through gaps to the front.
   - A controller that wins in a lane-based test may lose here. EquiFlow (Hyderabad, 2026) found plain fixed-time beat its AI.
3. **Ambulance priority has a hidden cost that nobody measures.**
   - Bengaluru has about 3,000 ambulance trips a day. BTP piloted 10 geofenced signals and is writing an SOP for ambulances ([DH](https://www.deccanherald.com/opinion/no-green-for-the-ambulance-3403011), [pilot](https://webjosh.com/article/in-a-pilot-project-bengaluru-traffic-police-geofence-10-signals-around-k-c-general-hospital-to-give-clearance-for-ambulances-1721410246-18077)).
   - Nobody has published how much the cross-street traffic loses, or how long it takes to recover.

**One line:** *Cities have no fair, open way to test signal controllers on Indian traffic, including what ambulance priority costs everyone else.*

## 2. Our solution (in plain words)

**Saarathi = a fair, open test track for traffic signals in Indian traffic (Part A), and a safe AI signal controller raced on it (Part B).**

- **Part A, the test track:**
  - Real Bengaluru map areas in SUMO, with bikes filtering through gaps and traffic load counted in PCU.
  - The same traffic and the same random seeds for every controller, and honest statistics.
  - It also checks whether the winner changes when our traffic assumptions change.
- **Part B, our controller:**
  - The AI never sets lights directly. At each decision it **picks between safe rules**: "serve the biggest queue" or "serve the biggest queue plus the incoming platoon from my neighbour".
  - A safety shell always enforces minimum and maximum green, yellow and all-red.
  - Junctions share 3 numbers with their neighbours: PCU released, arrival time and an ambulance flag.
  - Ambulance mode reports **ambulance time saved, the delay it caused others, and the minutes until traffic recovered**.

**The paper is useful whatever the result.** If our AI wins, that is shown fairly. If it loses or ties, the paper reports that, and we explain why, which is still new evidence for Indian traffic.

## 3. Paper title and research questions

**Working title:** *Does the Ranking Hold? A Fair, Open Benchmark of Traffic-Signal Controllers for Lane-less Indian Mixed Traffic, with a Safe Learning Controller and the Cost of Ambulance Priority*

- **RQ1:** Under Indian mixed, lane-less traffic, how do fixed-time, actuated and PCU max-pressure rank, with honest statistics?
- **RQ2:** Does that ranking change when bike filtering, PCU values or demand change?
- **RQ3:** Does a safe AI that picks between max-pressure rules beat tuned max-pressure, including on an area it never trained on?
- **RQ4:** What does ambulance priority cost other traffic, and how fast does the junction recover?

## 4. Features

### Must-have (the project is not done without these)
| # | Feature | Part | Exists today? | Days |
|---|---|---|---|---|
| A1 | 4 real areas (Old Airport Road pair, Silk Board, Trinity, Domlur), with the same routes, warm-up, demand cut-off and drain time for all | A | ◐ manifests exist | 3–5 |
| A2 | Fix the Domlur gridlock, or report it as a stress test. Count every failed run | A | ❌ | 3–5 |
| A3 | Honest statistics: 10 paired seeds × 2 demand levels, 95% CI, completed/scheduled count, failed runs reported | A | ❌ (5 seeds, not significant) | 3–4 |
| A4 | Robustness sweep: filtering on/off, PCU vs vehicle count, a second PCU set | A | ◐ profiles exist | 4–6 |
| A5 | Real counts at **one** Old Airport Road junction, counted live by eye (no video kept), with one time window held back for testing | A | ❌ | 1 weekend + 3 |
| A6 | Pune open counts (CC BY 4.0) as a second-city sanity check | A | ❌ | 2 |
| A7 | One command rebuilds the results table. Pinned versions, committed, licensed, run on a teammate's laptop | A | ❌ uncommitted | 2–3 |
| B1 | **Safety shell fix:** max-green is not enforced for PPO today (`env.py` never calls `must_rotate()`). Fix it and test with "hold forever" requests | B | ❌ bug | 2–3 |
| B2 | PPO picks between 2 safe rules (local MP vs MP plus the neighbour's platoon). One shared policy for all junctions | B | ❌ (raw phases, 1 junction) | 5–8 |
| B3 | Neighbour messages (PCU released, arrival time) | B | ❌ | in B2 |
| B4 | Train on 3 areas and test on a 4th it never saw. 3 training seeds | B | ❌ | 5–8 |
| B5 | Ambulance flag and route-ahead priority. Measure ambulance time, the delay to others and the recovery time | B | ❌ | 6–9 |

### Nice-to-have (only if ahead of schedule)
- Sensing tiers, meaning it still works with rough counts.
- A second field junction.
- Studio playback of the results.
- The NCR UAV trajectories, to tune bike gaps.

### Never build now
A dashboard, city scale, nightly retraining, fairness modules, live deployment.

## 5. The one main results table

| Controller | Delay incl. waiting to enter (s/trip) | Δ vs tuned MP (95% CI) | Trips finished / scheduled | Failed runs /10 | Ranking changes under sweep? |
|---|---|---|---|---|---|
| Fixed-time (city-style plan) | | | | | |
| Actuated | | | | | |
| Tuned PCU max-pressure | | | | | |
| Message-aware MP (no AI) | | | | | |
| **Saarathi (safe AI selector)** | | | | | |

There is also one ambulance table, with a row per priority policy and these columns: ambulance travel time, extra vehicle-minutes for others, recovery minutes.

The "message-aware MP (no AI)" row is there so we can tell how much gain comes from the **messages** and how much from the **learning**.

## 6. What is new, and what is not (be honest in the viva)

- **Not new on its own:**
  - Safe AI over max-pressure (Com-MP, [PP] 2610.31037).
  - Neighbour messages (CoLight, HALight).
  - Ambulance recovery (Lee & Chiu, Jiang).
  - Benchmarks for lane-based traffic (Sim2Signal [PP] 2609.01676, sumoITScontrol [PP] 2604.23240).
  - Ranking shifts in lane-based tests (Task Underspecification [PP] 2210.08607).
- **New (not found anywhere in the 2025–26 search):**
  - An open, multi-area SUMO benchmark for **lane-less Indian traffic**, with PCU and bike filtering.
  - A test of whether controller rankings **survive** those assumptions.
  - The cost and recovery of ambulance priority, **measured in that traffic**.
- **Never claim:** first Indian simulator or AI, beats BATCS, digital twin, deployment, novel communication, novel ambulance recovery, novel safety shell.

## 7. Timeline (24 Nov 2026 → paper by mid-Feb 2027)

| Weeks | Person 1 (Part A) | Person 2 (field + data) | Person 3 (Part B) |
|---|---|---|---|
| 1 (now) | Commit everything; time one full paired run | Choose the OAR junction; get a BGIT letter; inform the police | B1: safety-shell max-green fix |
| 2–3 | A1 + A2: same protocol everywhere, fix Domlur | A5: count the junction live (3 time windows) | B2/B3: two-rule selector and messages |
| 4–5 | A3: 10 seeds × 2 demand levels | A5/A6: calibrate on counts and check the held-out window; Pune check | B4: train on 3 areas, test on the 4th |
| 6–7 | A4: robustness sweep | A7: rerun on a clean laptop | B5: ambulance priority and cost |
| 8 | All three: the final race, both tables, figures | | |
| 9–11 | All three: write the paper, submit | | |

**If time runs out, cut in this order:** B5 first, then the 4th area, then A6. Never cut A3, B1 or the held-out window.

## 8. Where to publish

1. **SUMO User Conference 2027**, Berlin, 7–9 June. We expect the call around Nov–Dec 2026 and the deadline around mid-Feb 2027 (based on past years; check when the call comes out). This is the best fit.
2. **Backup:** the next TPMDC (IIT Bombay) or CTRG cycle. Their dates are not yet announced.
3. **Stretch:** IEEE ITSC 2027, reported deadline about 1 March (unverified). Later: the journal *Transportation in Developing Economies* (Springer).
4. Check indexing (Scopus/UGC-CARE) and fees on the official site before submitting. Avoid paid fast-acceptance journals.

## 9. Risks and fallbacks

| Risk | Fallback |
|---|---|
| The AI ties or loses | Report it with the confidence interval and keep the simplest rule that competes. The benchmark is still the paper. |
| The field counts don't match the simulator | Publish the mismatch and the sensitivity, and give no timing advice for that corridor |
| Gridlock spoils the delay numbers | Count the failed runs and report that traffic level as a stress test |
| Training is too slow on laptops | Use libsumo, separate processes, 1-hour episodes and small subnetworks. Drop an area before dropping seeds |
| The SUMO 2027 deadline differs | Go to the backup venue. The work does not change |

## 10. The 30-second pitch

> "Bengaluru spends crores on smart signals, but nobody outside can check the claims of 25% or 33% better travel. The standard tests assume cars stay in lanes, and here most vehicles are bikes squeezing through gaps. We built Saarathi, an open test track on real Bengaluru junctions where any signal controller can be raced fairly. We checked it against real counts we took ourselves. We also built a safe AI controller that can never break signal safety rules, and we measure what ambulance priority costs everyone else. Whoever wins, a city gets an honest answer before it buys."

**Likely viva questions:**
- **"Did you beat BATCS?"** No. BATCS publishes no data, so nobody can compare against it fairly. Our tool is how such a comparison could be done.
- **"Is it a digital twin?"** No. It is a Bengaluru-*inspired* test, checked against one real count.
- **"What if your AI loses?"** Then we report that, which is still useful. EquiFlow saw the same thing, and we explain *why* it happens.
