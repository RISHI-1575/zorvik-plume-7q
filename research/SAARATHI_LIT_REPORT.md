# Saarathi: Literature Report (Part A, Part B, overall)

2026-11-16. Short version. Details: `PART_A_LIT_GAP_REVIEW.md`, `part_a_refs.bib`.
Sources used: OpenAlex, Crossref, firecrawl research search, web. Not reachable: Scopus, WoS, IEEE, Google Scholar. Preprints are marked *preprint*.

## Verdict
The idea is publishable, but only as **"an open benchmark protocol plus evaluation axes"**. It is not publishable as "first open Indian laneless RL environment" or "novel controller". Part B alone has no novelty and is only a reference method.

## Part A: benchmark
- **Biggest threat:** Nandakumar et al., arXiv:2509.21745 (*preprint*). It is an open laneless Chennai single-junction SUMO+RL setup. It has no multi-junction scenarios, no plug-in API, and no max-pressure or fixed-time baselines.
- **Repo check:** the `RLTSCQ` repo has no licence, so we cannot copy it. Its flow files define only 4 passenger car vTypes and no sublane settings, so it may not contain the setup the paper describes. This is unconfirmed.
- **Gaps nobody fills** (ranked):
  1. Sensing-tier degradation curve in non-lane traffic.
  2. Worst-seed / stability reporting.
  3. Multi-junction plug-in benchmark with fixed baselines.
  4. Unseen-area zero-shot protocol.
  5. PCU sensitivity.
- **Field-calibrated and open and multi-junction:** nobody has this, and we don't yet either (A2/A3 pending).

## Part B: controller (Saarathi PPO)
| Component | Prior art | Status |
|---|---|---|
| Safety shell / action masking | Müller & Sabatelli 2022 (arXiv:2206.10122, *preprint*); Müller 2021 real-world deployment | Not novel; engineering only |
| Neighbour communication | CoLight (Wei 2019), MA2C (Chu 2020), Bokade 2023; HC-STGRL 2026 (Frontiers AI, Crossref-verified) | Not novel. Fixed 3-field messages are a design choice, not a claim |
| Ambulance priority | Qin & Khan 2012; EMVLight (Su 2023); Kiani 2023; Jiang 2026 (PLOS One, Crossref-verified) | Not novel. The cross-street recovery metric is the only possible twist; I did not find it reported, but coverage is limited |
| PCU-aware state in India | Savithramma & Sumathi 2023; Agarwal 2024 | Not novel |
| Beating max-pressure | Agarwal 2024 already hybridises max-pressure with PPO | Risk. Tuned max-pressure may be too strong |

Part B is therefore a **demonstration controller**, as RULES.md already says. Keep it parked until A2/A3 are done.

## Overall idea: what to claim
**Safe claim:** an open, multi-junction, plug-in benchmark for weak-lane-discipline traffic. It uses a fixed multi-seed protocol with worst-seed reporting and a sensing-tier axis. Concurrent single-junction open work exists (Nandakumar, *preprint*).

**Do not claim:**
- "first open laneless/Indian environment"
- "field-calibrated" (until the A3 gates pass)
- novel communication, ambulance recovery or safety shell
- "digital twin", deployment, or "beats BATCS"

**Main risk:** the same IIT Madras group lists our gaps as future work. Freeze the sensing-tier and worst-seed definitions in a dated commit soon.

## Next 4 actions
1. Reword C1 in `PART_A_COMPLETION.md` (recommendation only; I did not edit it).
2. Ask the Nandakumar authors for a licence, or ignore their files.
3. Do field counts (A2); this is the critical path.
4. Re-run the queries in Scopus/WoS before submission.
