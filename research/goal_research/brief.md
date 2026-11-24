# Brief: finalise Saarathi's goal (read fully)

Project: Saarathi, final-year capstone, 3 students, BGIT Bengaluru (VTU), 2025-26. ~6-8 weeks of work left. Repo: /Users/rishi/Personal/final year project/Saarathi (read PROJECT_DEFINITION.md, FINAL_PLAN.md, RULES.md, research/IMPROVEMENT_PLAN.md, research/DEEP_GAP_REVIEW.md, research/PART_B_COMPARISON.md, research/PART_A_DEEP_ANALYSIS.md if you have file access).

Today: Part A = SUMO sublane benchmark for Indian mixed traffic (PCU, two-wheeler filtering profile, seepage metric ~3.2x stock SUMO), real Bengaluru OSM areas (domlur, silk_board, old_airport_road, trinity, hebbal, corridor4), baselines fixed/actuated/PCU max-pressure, a web "Studio". Weak spots: stats not significant (few seeds), Domlur gridlocks (8-52% unfinished, teleports), no field calibration, uncommitted code.
Part B = PPO per junction + safety shell + neighbour messages (released PCU, ETA, ambulance flag) + ambulance cost (delay to others + recovery time). Only smoke-tested.
Decision: ONE paper covering both. Plan: Part B = AI picks between safe max-pressure-style options (Com-MP style, arXiv 2610.31037).
Rivals: Nandakumar arXiv:2509.21745 (Chennai single junction laneless RL), EquiFlow GIJET 2026 (Hyderabad 4 junctions PPO+EV, fixed-time beat PPO), Agarwal ESWA 2024, Guin 2026 Computer Networks (field-calibrated SUMO seepage).
Never claim: first Indian sim/RL, beats BATCS, digital twin, deployment, novel learned communication, novel ambulance recovery.

GOAL OF THIS RESEARCH: find the single best, practically buildable (3 students, ~8 weeks, laptops, SUMO, free data), publishable goal that solves a REAL problem people in Indian cities actually have, which the team can pitch with confidence to a viva panel, a conference, and a city official. Redesign is allowed. Be honest and concrete; label preprints [PP] vs published [P]; cite URLs for every external fact. No hype.
