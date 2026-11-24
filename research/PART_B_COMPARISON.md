# Part B vs existing systems and papers (2026-11-24)

**Key**
- ✅ = yes
- ◐ = partly
- ❌ = no
- ? = not confirmed by us

**Labels:** **[P]** = published, **[PP]** = preprint, **[D]** = deployed commercial or city system.

**Sources:** facts come from abstracts and limitations sections, as recorded in `DEEP_GAP_REVIEW.md`. Deployed systems are described only at the level of public information; vendor internals were not checked.

**Column meanings:**
- **Mixed / laneless:** handles Indian mixed traffic without lanes.
- **Learns:** uses learning (RL).
- **Safety guarantee:** hard safety rules or a stability proof.
- **Talks to neighbours:** junctions share information.
- **Ambulance:** emergency-vehicle priority.
- **Recovery / cost metric:** measures the delay an ambulance causes others and how fast traffic recovers.
- **Cheap sensing:** still works with rough counts instead of lane-level detectors.
- **Junctions:** how many junctions it was tested on.
- **Unseen-area test:** tested on an area it was not trained on.
- **Open code:** code is publicly released.
- **Field tested:** tested on real streets.

| System / paper | Status | Mixed / laneless | Learns | Safety guarantee | Talks to neighbours | Ambulance | Recovery / cost metric | Cheap sensing | Junctions | Unseen-area test | Open code | Field tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fixed-time (Webster) | classic | ❌ | ❌ | ✅ fixed timings | ❌ | ❌ | ❌ | ✅ none needed | any | — | ✅ | ✅ everywhere |
| Actuated (gap-based) | classic | ❌ | ❌ | ✅ min/max green | ❌ | ◐ | ❌ | ◐ loop detectors | any | — | ✅ | ✅ |
| Max-pressure (Varaiya 2013, TR-C) | [P] | ❌ | ❌ | ✅ stability proof | ◐ downstream queues | ❌ | ❌ | ❌ lane queues | network | ✅ no training | ✅ | ◐ pilots |
| SCOOT (UK) | [D] | ❌ | ❌ (model-based) | ✅ | ✅ central | ◐ | ? | ❌ loop detectors | city | — | ❌ | ✅ |
| SCATS (Australia) | [D] | ❌ | ❌ | ✅ | ✅ central | ◐ | ? | ❌ stop-line detectors | city | — | ❌ | ✅ |
| BATCS (Bengaluru, ~103 junctions) | [D] | claimed | ? | ? | ? | ? | ? | cameras ? | ~103 | — | ❌ | ✅, but no public numbers |
| PressLight (KDD 2019) | [P] | ❌ | ✅ | ❌ | ◐ | ❌ | ❌ | ❌ lane level | arterial | ❌ | ✅ | ❌ |
| MPLight (AAAI 2020) | [P] | ❌ | ✅ | ❌ | ◐ pressure | ❌ | ❌ | ❌ | 2,510 (Manhattan) | ◐ | ✅ | ❌ |
| CoLight (CIKM 2019) | [P] | ❌ | ✅ | ❌ | ✅ graph attention | ❌ | ❌ | ❌ lane counts | 196 | ❌ | ✅ | ❌ |
| HC-STGRL (Front. AI 2026) | [P] | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ◐ 20% sensor failure | network | ? | ? | ❌ |
| HALight (2026) | [PP] | ❌ | ✅ | ❌ | ✅ one-hop | ❌ | ❌ | ◐ missing lanes | network | ? | ? | ❌ |
| Com-MP (Zhu & Tan 2026) | [PP] | ❌ | ✅ | ✅ stability kept | ◐ | ❌ | ❌ | ✅ degraded sensing | network | ✅ | ? | ❌ |
| MAPPO-LCE (Satheesh 2025) | [PP] | ❌ (future work) | ✅ | ❌ (future work) | ✅ | ❌ | ❌ | ❌ | network | ? | ? | ❌ |
| Chaudhuri 2022 (Bengaluru geometry) | [P] | ❌ single-lane cars | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 1 | ❌ | ? | ❌ |
| Nandakumar et al. (Chennai, laneless) | [PP] | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ◐ approach queue | 1 | ❌ | ◐ no licence | ❌ (sim only) |
| EquiFlow (Hyderabad, GIJET 2026) | [P] | ✅ | ✅ PPO | ? | ? | ✅ | ? | ? | 4 | ❌ | ? | ❌ — fixed-time beat PPO |
| SIGMA (Kolkata-modelled) | [PP] | ◐ | ✅ + LLM | ❌ | ◐ | ✅ | ❌ | ❌ | 4 | ❌ | ? | ❌ |
| Agarwal et al. (ESWA 2024) | [P] | ✅ heterogeneous | ✅ | ? | ? | ❌ | ❌ | ? | ? | ? | ? | ❌ |
| EMVLight (Su, TR-C 2023) | [P] | ❌ | ✅ | ❌ | ✅ | ✅ routing + signals | ◐ ordinary delay | ❌ | network | ❌ | ✅ | ❌ |
| Lee & Chiu 2020 (Sensors) | [P] | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ flow compensation | ◐ | corridor | — | ❌ | ✅ field |
| Jiang 2026 (CPC meta-RL, PLOS ONE) | [P] | ❌ | ✅ | ❌ | ? | ✅ | ✅ disturbance term | ❌ | network | ◐ meta-RL | ? | ❌ |
| Dai et al. 2025 (PLOS ONE) | [P] | ❌ | ❌ | ✅ | ❌ | ✅ single EV | ◐ | ❌ | corridor | — | ? | ❌ |
| **Saarathi Part B (planned)** | ours | ✅ PCU + sublane + bike filtering | ✅ PPO | ✅ safety shell + max-pressure fallback | ✅ PCU released / ETA / ambulance flag | ✅ | ✅ cross-street cost + recovery time | ✅ sensing tiers (planned) | 4–6 real Bengaluru map areas | ✅ train on 3, test on a 4th | ✅ licensed | ❌ sim only |

## What this shows

1. **No single Part B feature is new.**
   - Safety plus learning already exists: Com-MP.
   - Neighbour messages already exist: CoLight, HALight.
   - Ambulance recovery already exists: Lee & Chiu, Jiang.
   - Mixed traffic already exists: Nandakumar, EquiFlow.
2. **The combination is new.** No row has ✅ for all four of these:
   - mixed/laneless traffic;
   - a safety or stability guarantee;
   - multi-junction with an unseen-area test;
   - open code.

   Nandakumar and EquiFlow are closest, but neither has the safety guarantee, the unseen-area test or a licensed release.
3. **Biggest risk:** EquiFlow found that fixed-time beat PPO in Hyderabad. Building Part B *on top of* max-pressure (the Com-MP style) is our protection against the same result.
4. **Deployed systems (SCOOT, SCATS, BATCS) are closed and lane-detector-based.** BATCS publishes no performance numbers. We cannot compare against them, so we never claim to beat them.

**Safe claim:** "a safe, open, multi-junction learning controller for Indian mixed traffic, fairly compared with strong classical baselines". **Never claim:** first, novel, or better than BATCS.
