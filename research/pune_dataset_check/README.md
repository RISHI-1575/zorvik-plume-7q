# Pune Heterogeneous Traffic Count Dataset — fit check (2026-11-11)

Source: Matange, A. & Abraham, J. (2026). *Heterogeneous Traffic Count Dataset, Pune (Jan 2023)*. Mendeley Data V1. DOI 10.17632/xnf2k6n288.1. CC BY 4.0. CCTV from Pune Traffic Police Commissioner.
Download: 3 files (traffic.zip sha256 `648e9c33…cc03c4`, 15.6 MB → 115 CSVs). Raw data not committed; re-download from the DOI.

## What the files really are
- Rows are **per video frame** (~25 fps × 4 directions), not 5-minute counts. Each column is a **running total** that restarts per file. Real count = last value. `*_one.csv` continues the main file.
- Coverage: **09:00–12:00 only**, 8 days (11–18 Jan 2023; 14–15 = weekend/Sankranti), 8 cameras: Alankar a2,a3 · Jehangir j1,j2,j3 · RTO r1,r2,r3. 192 camera-hours, 470,654 vehicles, no counter resets.
- Classes: car, motorbike, bus, truck. **No auto-rickshaw** (absorbed into car/motorbike).
- Direction = UP/DOWN/LEFT/RIGHT **on screen**, not compass or turning movement. Camera views are not published.

## Quality
| Camera | veh/h mean | day-to-day CV | 2W share | Verdict |
|---|---|---|---|---|
| a2 | 806 | 38% | 52% | usable, noisy |
| **a3** | **6,289** | 28% | **19%** | **reject — implausible, likely tracker double counting** |
| j1 | 2,797 | 21% | 44% | usable |
| j2 | 1,661 | 16% | 47% | good |
| j3 | 2,000 | 13% | 47% | good |
| r1 | 1,429 | 33% | 39% | usable, noisy |
| r2 | 2,782 | 17% | 46% | good |
| r3 | 1,570 | 16% | 57% | good |

Overall 2W share 38% (car 49%) — below typical Indian urban mixes; YOLO likely under-counts two-wheelers under occlusion. Treat class split as biased.

## Geography
Jehangir Chowk → Alankar Chowk ≈ 400 m (Connaught Rd); Alankar Chowk → RTO Chowk ≈ 1.3–1.7 km (NH 753F / Ambedkar Rd). All three are around Pune Railway Station: a real connected 3-junction stretch. Bbox ≈ S 18.525 W 73.861 N 18.535 E 73.879 (~1.5 km², under `make_area.py` 4 km² cap). Intermediate signals on the Alankar–RTO leg not yet verified.

## Fit to Saarathi `corridor.yaml`
| Needed | Pune gives |
|---|---|
| `peak_flows_veh_per_hour` | ✅ real AM-peak approach volumes (7 good cameras) |
| demand profile | ⚠️ 09–12 only, at any resolution (15-min possible); no 24 h |
| `modal_split` (6 classes) | ⚠️ 4 classes, 2W biased low, no autos |
| turning movements | ❌ screen directions only — need camera views |
| signal timings / headways | ❌ none |
| held-out validation | ✅ calibrate on some weekdays, test GEH on another |

Reproduce: `python3 -I summary.py <unzipped>/traffic out.csv` and `python3 -I flows.py <unzipped>/traffic`.
