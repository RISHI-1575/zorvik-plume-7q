# Saarathi Part A — Literature Search & Research-Gap Review

**Date:** 2026-11-16 · **Scope:** Part A only (open, configurable SUMO benchmark for Indian mixed / weak-lane-discipline traffic; Studio; plug-in controller API; 5-seed fixed / actuated / max-pressure baselines). Part B (PPO) is parked and not assessed here.
**Companion file:** `part_a_refs.bib` (52 entries: 45 Crossref-verified, 7 labelled preprint/unverified).
**Constraint followed:** `RULES.md` §2 never-claim list. Nothing in the project was edited; this review only *recommends* wording changes.

> **Headline.** The claim "first open benchmark for non-lane heterogeneous traffic with field calibration" (`PART_A_COMPLETION.md` §3 C1, §4) is **no longer safe**. A Nov-2026 arXiv *preprint* (Nandakumar, Banerjee & Vanajakshi, arXiv:2509.21745) releases an open laneless-heterogeneous SUMO + RL signal-control framework built from field flow data in India. It is single-junction and has no benchmark protocol, but it removes "first open laneless SUMO+RL" as a differentiator. Part A is still publishable on what it adds beyond that: multi-junction, plug-in API, fixed multi-seed protocol with worst-seed reporting, sensing-tier axis, unseen-area protocol. See §5–§6.

---

## 1. Workflow log (the 8 steps)

### Step 1 — Topic, concepts, keywords
Topic: *open, reproducible benchmarking of traffic-signal controllers under Indian mixed / non-lane-based traffic in SUMO.*

| Concept | Keywords / synonyms |
|---|---|
| Traffic type | "non-lane-based", "lane-less", "laneless", "weak lane discipline", "less lane-disciplined", "heterogeneous", "mixed traffic", "disordered", "motorcycle-dominated", "two-wheeler", "seepage", "filtering", "PCU", "PCE", "Indo-HCM", "IRC 106" |
| Signal control | "traffic signal control", TSC, "adaptive signal", "max-pressure", "actuated", "Webster", "reinforcement learning", MARL, "PressLight", "CoLight" |
| Benchmark / reproducibility | benchmark, "open-source", "reproducible", "library", RESCO, LibSignal, "plug-in", "protocol", "seeds", "variance" |
| Simulator / calibration | SUMO, "sublane", SL2015, SiMTraM, "calibration", "GEH", "validation", "field data" |
| Sensing / robustness | "partial detection", "missing data", "noisy sensors", "detector failure", "sensing" |
| Generalisation | "zero-shot", "cross-city", "transfer", "unseen" |
| Place | India, Bengaluru / Bangalore, Chennai, Kozhikode, Tumakuru, Ludhiana, Vietnam, Indonesia (comparable regimes) |

### Step 2 — Query strings actually run
Boolean form (as intended for Scopus/WoS) and the practical short forms run on OpenAlex / Crossref / firecrawl (long Boolean strings are poorly handled by OpenAlex relevance search; see Errors).

Boolean master queries:
- Q-A `("traffic signal" OR "signal control") AND ("reinforcement learning" OR benchmark OR "max-pressure") AND (heterogeneous OR "non-lane" OR "lane-less" OR laneless OR "mixed traffic" OR "weak lane discipline" OR India)`
- Q-B `(SUMO OR "SiMTraM") AND (calibration OR validation) AND ("mixed traffic" OR heterogeneous OR "non-lane-based" OR India)`
- Q-C `("traffic signal control") AND (benchmark OR library OR "open-source") AND (reproducib* OR seeds OR variance OR "plug-in")`
- Q-D `("traffic signal control") AND ("partial detection" OR "missing data" OR "noisy" OR "sensor failure" OR "detector")`
- Q-E `("traffic signal control") AND ("zero-shot" OR "cross-city" OR transfer OR generali?ation)`

Run forms (OpenAlex / firecrawl / web): `motorcycle dominated traffic signal control reinforcement learning SUMO` · `Max Pressure mixed traffic motorcycles occupancy` · `Ho Chi Minh Hanoi traffic signal reinforcement learning motorbikes` · `Bengaluru traffic simulation SUMO signal` · `India traffic signal control deep reinforcement learning real intersection field data` · `Bangalore adaptive traffic control system BATCS` · `traffic signal control robustness benchmark noisy sensors detector failure reinforcement` · `cross-city transfer traffic signal control benchmark` · `SUMO-RL Gymnasium environment traffic signal` · `laneless heterogeneous traffic SUMO open framework reinforcement learning India` · firecrawl research queries on partial detection and SUMO calibration for heterogeneous traffic.

### Step 3 — Databases: used vs not used
| Used | Not used / not reachable |
|---|---|
| OpenAlex (search, metadata, cited-by) · Crossref (DOI verification, bibliographic lookup) · firecrawl research search (paper search + full-text read of arXiv) · general web search | **Scopus, Web of Science, IEEE Xplore, ScienceDirect, Google Scholar** (no access from this session). Alert strings for them are given in §8 but were **not run**. |

Consequence: recall is bounded by OpenAlex/firecrawl coverage. Re-run Q-A…Q-E in Scopus/WoS before submission.

### Step 4 — Search fields
Title / abstract / keyword fields via OpenAlex `title_and_abstract.search`; author searches for **T. V. Mathew, Arasan (V. Thamizh Arasan), Kanagaraj, Asaithambi, Savithramma, Ault & Sharon** (+ Vanajakshi, Padinjarapat found while chasing). Author hits that mattered: Padinjarapat & Mathew (saturation flow), Kanagaraj & Treiber (mixed-traffic model), Savithramma & Sumathi (RL), Ault & Sharon (RESCO). OpenAlex author metadata was unreliable for two records; **all bibliographic data in the .bib comes from Crossref, not OpenAlex.**

### Step 5 — Refinement
2018–2026 (older seeds kept only for SUMO-era foundations: Qin & Khan 2012, SiMTraM 2012); peer-reviewed journal / conference preferred; arXiv kept only when it is the sole source and then labelled *preprint*; reviews kept for context (Noaeen 2022, Xiao 2025); theses / pure vendor material dropped.

### Step 6 — Screening
~120 candidates → title/abstract screen → **48 kept** (45 Crossref-verified + 3 preprints used in the analysis; 4 more preprints/unverified in the .bib for completeness). Citation counts were used to sort within clusters but are **not reproduced** here (they differ by source and drift weekly).

### Step 7 — Citation chasing
- **Forward (cited-by, OpenAlex, top 25 each):** RESCO, LibSignal, Savithramma & Sumathi 2023, Agarwal 2024, Padinjarapat & Mathew, SiMTraM-vs-SUMO (Patel 2016). Guin 2026 (Computer Networks) has 0 citations yet (new).
- **Backward:** done by reading reference lists of the threat paper (2509.21745) and the SUMO-calibration papers; not exhaustive for RESCO/LibSignal.
- Chasing produced: Chaudhuri 2022, Sashank 2020, Chowdhury 2024, Shahdah 2026, Khadhir 2022, Kurniawan 2025, and the threat preprint (via firecrawl, not OpenAlex — OpenAlex had not indexed it).

### Step 8 — Management / alerts
BibTeX: `part_a_refs.bib`. Alert strings: §8.

### Errors / limits (honest log)
- OpenAlex relevance is noisy for long queries (a place-name query returned silk-biology papers) → short and author-based queries used.
- A probe DOI I invented while testing returned 404; it is **not** in any output.
- 45 DOIs resolved through Crossref; metadata in .bib is Crossref's. Page numbers/volumes deliberately omitted (not fetched).
- Full text was read only for arXiv:2509.21745. Everything else is judged from title/abstract/metadata — so matrix cells marked `?` are "not checked", **not** "no".

---

## 2. Screened table (kept papers, grouped)

Verification: **V** = Crossref-verified DOI; **P** = preprint; **U** = unverified. BibTeX key in the .bib.

### A. Benchmarks, libraries, simulators
| Key | Year | Venue | Note |
|---|---|---|---|
| lopez2018sumo V | 2018 | ITSC | SUMO reference |
| zhang2019cityflow V | 2019 | WWW | CityFlow |
| ault2021resco U (no DOI) | 2021 | NeurIPS D&B | RESCO — benchmark genre precedent, SUMO, lane-based |
| mei2023libsignal V | 2023 | Machine Learning | LibSignal, cross-simulator |
| bokade2025pytsc V | 2025 | Sensors | PyTSC unified MARL platform |
| riehl2026 V | 2026 | SUMO Conf. | sumoITScontrol controller collection |
| nguyen2025trex P / nguyen2026 V | 2025/26 | arXiv / ETRR | T-REX robustness-under-incidents benchmark (lane-based) |
| roosta2023 V | 2023 | SUMO Conf. | bicycle modelling in SUMO |

### B. RL signal control (methods, surveys)
chu2020ma2c V · wei2019presslight V · wei2019colight V · bokade2023 V · mo2022cvlight V · li2021 V · shen2023 V (heterogeneous intersections, IET ITS — country/non-lane status not checked) · noaeen2022 V (review) · xiao2025review V (review; Crossref year 2024) · ren2025 V (cooperation vs independence) · jiang2024 V · da2024 V · sun2024crosslight V · shi2024 V (generalisability + robustness) · müller2021 V (real-world deployment of RL TSC)

### C. India / non-lane / heterogeneous: simulation, calibration, flow theory
| Key | Year | Venue | Note |
|---|---|---|---|
| padinjarapat2020 V | 2020 | Transportmetrica B | saturation flow, non-lane mixed traffic (India) |
| khadhir2022 V | 2022 | J. Adv. Transp. | delay model, less-lane-disciplined |
| patel2016 V | 2016 | Transp. Res. Procedia | SUMO vs SiMTraM, Indian traffic |
| sashank2020 V | 2020 | LNCE | SUMO calibration, Indian heterogeneous traffic |
| chowdhury2024 V | 2024 | Transp. Eng. | SUMO calibration, heterogeneous (non-India, per title; not checked) |
| shahdah2026 V | 2026 | Sustainability | SUMO CF/LC calibration, heterogeneous (country not checked) |
| guin2026seepage V | 2026 | Computer Networks | two-wheeler seepage modelling + "benchmarking" |
| singh2020 V | 2020 | Transp. Res. Procedia | seepage using available gaps |
| munigety2018 V · papathanasopoulou2018 V · kanagaraj2018 V · maiti2023 V · zhao2023 V · beza2025 V | 2018–25 | various | mixed-traffic behaviour / fundamental diagrams / lane-less vs lane-free |

### D. India / heterogeneous RL signal control
| Key | Year | Venue | Note |
|---|---|---|---|
| savithramma2023 V | 2023 | Green Energy & Intell. Transp. | Tumakuru junction; vehicle-type / PCU / multi-agent states |
| agarwal2024 V | 2024 | Expert Syst. Appl. | Ludhiana; hybrid max-pressure + PPO, video-derived demand |
| chaudhuri2022 V | 2022 | SIST (Springer) | **Bengaluru** intersection, SUMO, DQN/A2C |
| kurniawan2025 V | 2025 | Applied Sciences | hybrid rule+RL, developing-city setting (non-lane status not checked) |
| **nandakumar2026laneless P** | 2026 | arXiv:2509.21745 | **threat**, §5 |

### E. Sensing degradation / robustness / transfer
zhang2021partial V (partial vehicle detection) · rodrigues2019 V · shi2024 V · hu2026halight P (lane-level missing observations; lane-based) · jiang2024 V · da2024 V · sun2024crosslight V

### F. Emergency vehicles (context only, per RULES §2.3)
qin2012 V · su2023emvlight V · kiani2023 V

---

## 3. Gap matrix

Legend: ● yes (confirmed from abstract/full text) · ◐ partial · ○ no · ? not checked. Columns: **NL** non-lane / heterogeneous · **FC** field-calibrated · **OR** open/reproducible release · **MJ** multi-junction · **API** plug-in controller API / benchmark protocol · **SV** multi-seed variance reporting · **ST** sensing-tier / degraded-sensing evaluation · **UG** unseen-area generalisation · **IN** India-specific.

| Paper | NL | FC | OR | MJ | API | SV | ST | UG | IN |
|---|---|---|---|---|---|---|---|---|---|
| **Nandakumar 2026 (P)** | ● | ◐ field flows; no GEH-style gates seen | ● GitHub | ○ single junction | ○ | ◐ 5 seeds | ◐ queue-only reward; noisy queues "not tested" | ◐ demand surge, not area | ● Chennai |
| Savithramma & Sumathi 2023 | ◐ | ? | ? | ○ | ○ | ? | ○ | ○ | ● |
| Agarwal 2024 | ◐ | ◐ video demand | ? | ○ | ○ | ? | ○ | ○ | ● |
| Chaudhuri 2022 | ? | ◐ real junction | ? | ○ | ○ | ? | ○ | ○ | ● Bengaluru |
| Guin 2026 (seepage) | ● | ● field | ? | ○ | ◐ "benchmarking" of models | ? | ○ | ○ | ● |
| Sashank 2020 | ● | ● | ? | ○ | ○ | ○ | ○ | ○ | ● |
| Patel 2016 (SUMO vs SiMTraM) | ● | ◐ | ○ | ○ | ○ | ○ | ○ | ○ | ● |
| Padinjarapat & Mathew 2020 | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | ● |
| Khadhir 2022 | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | ● |
| Chowdhury 2024 / Shahdah 2026 | ● | ● | ? | ○ | ○ | ○ | ○ | ○ | ○ / ? |
| RESCO 2021 | ○ | ○ | ● | ● | ● | ◐ | ○ | ○ | ○ |
| LibSignal 2023 | ○ | ○ | ● | ● | ● | ? | ○ | ◐ cross-sim | ○ |
| T-REX / Nguyen (P/V) | ○ | ○ | ● | ● | ● | ◐ | ○ | ◐ shifts | ○ |
| PyTSC 2025 | ○ | ○ | ● | ● | ● | ? | ○ | ? | ○ |
| Zhang 2021 partial detection | ○ | ○ | ? | ? | ○ | ? | ● | ○ | ○ |
| HALight 2026 (P) | ○ | ○ | ● | ● | ○ | ? | ◐ missing lanes | ○ | ○ |
| Shi 2024 / Jiang 2024 / CrossLight | ○ | ○ | ? | ● | ○ | ? | ◐ | ● | ○ |
| **Saarathi Part A (target state)** | ◐ SUMO sublane | ○ pending A2–A3 | ● planned | ● 4-junction + any OSM area | ● | ● 5 seeds + worst-seed | ◐ planned 3 tiers | ◐ `make_area.py` | ● |

### Empty cells (the gaps)
| # | Gap (no paper found with all of these) | Closest prior work |
|---|---|---|
| G1 | **Non-lane traffic × sensing-tier degradation curve** (full state → stop-line counts → aggregate counts) over several controllers | Nandakumar (queue-only, noise untested); Zhang 2021 / HALight (degraded sensing, but lane-based) |
| G2 | **Non-lane × multi-seed *and worst-seed/stability* reporting** as a ranking criterion | Nandakumar (5 seeds, mean-based, high-variance noted); RESCO (lane-based) |
| G3 | **Non-lane × multi-junction × plug-in controller API with fixed scoring protocol** | RESCO/LibSignal/PyTSC (protocol, lane-based); Nandakumar (single junction, no API) |
| G4 | **Non-lane × unseen-area zero-shot protocol** | Shi/Jiang/CrossLight (lane-based transfer); Nandakumar (demand shift only) |
| G5 | **Field-calibrated *and* open *and* multi-junction in non-lane traffic** | Nobody has all three. **Saarathi does not have it yet either** (FC ○ until A2–A3). |
| G6 | **PCU-factor sensitivity of controller ranking** (RULES §3.3) | Savithramma (PCU as state), Padinjarapat (PCE estimation); none test ranking sensitivity |

---

## 4. Ranked gaps (novelty × feasibility, ~3 months, capstone team)

Scale 1–5. Score = novelty × feasibility.

| Rank | Gap | Novelty | Feasibility | Score | Why / risk |
|---|---|---|---|---|---|
| **1** | **G1 sensing-tier axis** | 5 | 5 | 25 | Observation masking in SUMO, uses existing controllers and harness; answers a real procurement question. **Risk:** Nandakumar lists "noisy/quantised queue estimates" as future work, so move early and fix the tier definitions in the repo now (timestamped). Do **not** present it as sensor-failure modelling (parked, RULES §1). |
| **2** | **G2 stability / worst-seed protocol** | 3–4 | 5 | ~18 | Already seeded by our own Domlur finding (1-seed ranking reverses over 5 seeds). Needs 10+ seeds on 3 areas and a simple statistic (worst-seed, CVaR, rank-flip rate). Nandakumar also plans "more seeds", so the novelty is the *ranking-stability argument*, not seed count. |
| **3** | **G3 multi-junction non-lane benchmark + plug-in API + protocol** | 3 | 5 | 15 | This is the Part A core and mostly built. After the threat it is a *completeness* claim ("multi-junction, API, protocol"), not a "first" claim. Needs the A5 clean-machine test to be credible. |
| **4** | **G4 unseen-area zero-shot** | 4 | 3–4 | ~14 | `make_area.py` makes areas cheap; the weak point is that uncalibrated areas must be labelled synthetic-informed (RULES §2.7, §4). Only meaningful once a learned/tuned controller exists (Part B) or for tuned max-pressure parameter transfer. |
| **5** | **G6 PCU sensitivity** | 2–3 | 5 | ~12 | Cheap, required by RULES §3.3 anyway; frame as an ablation, not a headline. |
| — | G5 field-calibrated open multi-junction | 5 | **2** | 10 | The strongest contribution **if** A2/A3 gates pass; it is the critical path and depends on field access, not on code. Keep it as the *credibility* leg, not the thing the paper depends on. |

**Recommended paper spine (still consistent with RULES §2 safe claim):** G3 as the artefact, G1 + G2 as the new evaluation axes, G6 as ablation, G5 as the credibility upgrade when A3 lands.

---

## 5. Threats to Part A claims

### T1 — HIGH: Nandakumar, Banerjee & Vanajakshi, arXiv:2509.21745 (*preprint*, v2, Nov 2026)
What it is (read in full-text passages): PPO signal control with a queue-based reward, SUMO SL2015 sublane config (lateral alignment arbitrary, resolution 0.8 m, minGapLat 0.5 m, left-hand), 4 classes (two-wheeler 64.0 %, car 25.7 %, auto 6.3 %, HMV 3.9 %) from field flow data, **one laneless junction near Chennai airport** + one lane-based junction in Kozhikode, 5 seeds, baselines Dynamic Webster / actuated / RESCO-DQN, higher-demand scenarios without retraining, code at `github.com/AnirudN/RLTSCQ`. Claims "first open laneless heterogeneous SUMO configuration integrated with RL signal control on a current SUMO version."
- **Threatens:** any "first open … for non-lane heterogeneous traffic" wording (PART_A_COMPLETION.md C1 and §4 uniqueness row "Traffic model"); the "no open resource exists" framing of §3 problem space.
- **Does not threaten:** multi-junction scope, plug-in API / protocol, fixed-time and max-pressure baselines (its own future work), worst-seed reporting, sensing tiers, unseen-area protocol.
- **Also exposes:** the same group (Vanajakshi, IIT Madras) works on the same regime and lists our gaps as future work. A competing benchmark in 6–12 months is plausible.
- **Caveats on my reading:** licence of the repo, whether its calibration meets GEH-style gates, and the exact SUMO configuration files were **not inspected**; check the repo before writing related work. It is a preprint and unrefereed.

### T2 — MEDIUM: Chaudhuri, Masti, Veerendranath & Natarajan 2022 (SIST, Springer; V)
SUMO + DQN/A2C on a real **Bengaluru** intersection. Threatens "first RL/SUMO on Bengaluru" phrasing (already on the RULES §2.1 never-claim list). Single junction, no non-lane focus found, no open protocol found (from metadata only).

### T3 — MEDIUM: Guin et al. 2026, Computer Networks (V)
"Modeling and benchmarking two-wheeler seepage behaviour in dense mixed traffic": field-calibrated SUMO seepage with a "benchmark" framing. Not signal control, and I did not confirm a code/data release. Threatens a "first calibrated seepage in SUMO" statement and any novelty claim on seepage realism. **Action:** read it before relying on the seepage validation recipe; cite and reuse its metrics rather than reinventing.

### T4 — PARTIAL (already on the never-claim list)
- Savithramma & Sumathi 2023; Agarwal 2024: Indian RL TSC with PCU/hybrid control — RULES §2.1.
- Sashank 2020; Chowdhury 2024; Shahdah 2026; the Sri Lankan SUMO-calibration papers (not verified, not in .bib): SUMO calibration for heterogeneous traffic without RL or a benchmark. Threatens "first to calibrate SUMO for mixed traffic" only.
- Patel 2016 (SUMO vs SiMTraM): SUMO's suitability for Indian traffic has been assessed before; do not claim SUMO-for-India is new.
- RESCO / LibSignal / PyTSC / T-REX: "open TSC benchmark" as a genre is established; only the *regime* is novel.

### Suggested wording changes (recommendation only; no file edited)
| Current (PART_A_COMPLETION.md) | Problem | Safer replacement |
|---|---|---|
| C1 "first open one for non-lane heterogeneous traffic with field calibration" | contradicted by T1 (open, laneless, field flows) and not yet true (calibration pending) | "An open multi-junction benchmark with a plug-in controller API and fixed multi-seed protocol for weak-lane-discipline traffic; concurrent single-junction open work exists (Nandakumar et al., preprint)." Add "field-calibrated at one corridor" **only** after A3 gates are reported. |
| §3 "There is **no open, reproducible, field-calibrated benchmark** for this regime" | too absolute | "To our knowledge, no open *benchmark protocol* (multi-junction, plug-in controllers, fixed seeds, worst-seed reporting) exists for this regime." |
| §4 uniqueness row "Traffic model" | implies exclusivity | keep the content, drop any implication that nobody has open laneless SUMO configs |
| C3 / sensing axis described as "genuinely novel" | true at time of search, but at risk (T1 future work) | "No benchmark we found evaluates controllers across sensing tiers in non-lane traffic (search 2026-11-16)." |

---

## 6. What to do next (literature-driven, small)
1. Clone `AnirudN/RLTSCQ`, check licence, scenario files, and the demand/calibration data; run their laneless net as an *additional Studio scenario* (cite it) — turns the threat into a baseline/related-work asset.
2. Run Q-A…Q-E in Scopus/WoS; check Nandakumar's reference list for Indian laneless RL papers I may have missed.
3. Read Guin 2026 and Kurniawan 2025 properly (non-lane status, code release).
4. Freeze the sensing-tier definitions (G1) in a dated commit before anyone else publishes them.
5. Verify RESCO's final venue string and SiMTraM's bibliographic record before citing as published.

---

## 7. Items deliberately left out of the bibliography
Seen in search results but not Crossref-verified and not read: Hickert 2026 "Calibration Illusion" (arXiv 2608.19642) · Sim2Signal (arXiv 2609.01676) · LemgoRL (arXiv 2103.16223) · arXiv 2109.14337, 2304.10722, 1910.10808, 2005.09624, 2405.10665 · TRAC 2026 (10.5815/ijisa.2026.05.03) · Sri Lanka conference papers (10.31705/trf.2026.1, .7) · Alegre 2021 (10.7717/peerj-cs.575) · Azfar 2025 (10.1080/15472450.2025.2559410) · Mattungal & Vanajakshi 2025 (10.1371/journal.pone.0319325) · Sugiarto PCE papers (10.1371/journal.pone.0306112, 10.1371/journal.pone.0256620) · Singh & Rao 2023 TRR. Verify through Crossref before using any of them.

---

## 8. Saved-search alerts (not run; for the team to set up)

**Scopus (alert):**
```
TITLE-ABS-KEY(("signal control" OR "traffic signal") AND ("reinforcement learning" OR benchmark OR "max-pressure") AND (heterogeneous OR "non-lane" OR "lane-less" OR laneless OR "mixed traffic" OR "weak lane discipline" OR India)) AND PUBYEAR > 2024
```
```
TITLE-ABS-KEY((SUMO OR SiMTraM) AND (calibrat* OR validat*) AND ("mixed traffic" OR heterogeneous OR "non-lane-based" OR "lane-less" OR India))
```
```
TITLE-ABS-KEY(("traffic signal control") AND ("partial detection" OR "missing data" OR "noisy" OR "detector failure" OR "sensing")) AND PUBYEAR > 2024
```
**Web of Science:** `TS=(("traffic signal control" OR "signal control") AND ("reinforcement learning" OR benchmark) AND (laneless OR "lane-less" OR "non-lane-based" OR "mixed traffic" OR India))`
**Google Scholar alerts:** `"laneless" "traffic signal" reinforcement learning SUMO` · `"non-lane-based" OR "lane-less" "signal control" benchmark` · author alerts: Vanajakshi, T. V. Mathew, Arasan, Savithramma, Kanagaraj, Ault Sharon. Also follow *cited-by* on arXiv:2509.21745, RESCO and LibSignal.
**arXiv listing watch:** `cs.LG`/`eess.SY` + "traffic signal" + "heterogeneous" or "laneless".
