# Saarathi — Improvement Plan (agreed 2026-11-24)

Status: a proposal agreed with the user in chat. It does not override `PROJECT_DEFINITION.md` → `FINAL_PLAN.md` → `RULES.md`; if it conflicts with them, they win. Gap IDs refer to `research/DEEP_GAP_REVIEW.md`.

## Decision
- **One paper covering both halves.** No separate papers for now.
- **Framing:** a fair, open test bench for Indian mixed traffic (Part A), plus a safe learning controller raced on it (Part B).
- The paper is publishable whether our controller wins or loses, because the fair-testing result is the core contribution.
- A second paper only if field counts or a strong controller result appear later.

## Honest rating (2026-11-24)
| | Now | After fixes |
|---|---|---|
| Part A — simulator / test bench | 6/10 | 8–9/10 |
| Part B — our controller | 2/10 | 6–7/10 |
| Paper as a whole | 3/10 | 7–8/10 |

## Part A fixes (cheapest first)
| Fix | Gap | Boost | Effort |
|---|---|---|---|
| Honest statistics: 10+ seeds, paired tests, 95% CIs, failed runs marked as failed | BG2, BG10 | +1 | 1 week |
| Busy-traffic demand levels where controllers separate | BG2 | +0.5 | 2–3 days |
| Ranking-robustness sweep: bike share, PCU values, filtering on/off | BG1, BG8′ | +1 | 1–2 weeks |
| Real counts at one Old Airport Road junction, public spot, no faces/plates, one held-out window | BG5, BG12 | +1 (largest credibility gain) | 1 weekend + video counting |
| Fix Domlur gridlock (demand or side roads) | BG10 | +0.3 | 2–3 days |
| Commit, licence, clean-machine rerun | BG5 | +0.2 | 1 day |

## Part B fixes
| Fix | Gap | Boost | Effort |
|---|---|---|---|
| Train PPO properly on several areas (not a smoke test) | — | +2 | 2–3 weeks |
| Stability-preserving design: the AI chooses *between* safe options (for example max-pressure variants) instead of setting raw phases. Cite Com-MP, arXiv 2610.31037; the new part is Indian mixed traffic. | BG7 | +1.5 | 1 week |
| Train on 3 areas, test on an unseen 4th | G4 | +1 | few days |
| Cheap-sensing tiers: still works with rough counts | BG3 | +1 | 1 week |
| Ambulance cost score: delay to everyone else, plus time for traffic to recover | BG6 | +0.5 | 1 week |

## Order of work
1. Part A statistics and failed-run fix (the foundation).
2. Busy demand levels, then the robustness sweep.
3. Field count at one junction (can run in parallel).
4. Build Part B inside the safety design.
5. Race every controller on Part A.
6. Write the paper.

Total: about 6–8 weeks with 3 people.

## Suggested team split
- Person 1: Part A statistics and the sweep.
- Person 2: real counts at one junction.
- Person 3: Part B controller.
- All three: the final race and the write-up.

## Target venues
- SUMO User Conference: best fit and easiest.
- TRB Annual Meeting: deadline around August.
- *Transportation in Developing Economies* (Springer).
- IEEE ITSC.

Check every venue against Scopus or UGC-CARE. Avoid fast-acceptance paid journals.

## Never claim
- first Indian simulator or RL controller
- beats BATCS
- digital twin
- deployment
- novel learned communication
- novel ambulance recovery
