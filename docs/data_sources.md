# Data sources for the Bengaluru mixed-traffic SUMO simulator

Compiled 2026-11-10 from open web sources. Every number carries a link and a status:
`sourced` (read in the source), `derived` (computed here, computation shown),
`registrations-not-road-share` (fleet counts, not what is on the road), `not-found`.
Nothing below is invented. Where a paper was paywalled, only what the abstract says is recorded.

## 1. Modal split of road traffic

| parameter | value | unit | source | year | status |
|-|-|-|-|-|-|
| Urban BMR observed vehicles, motorcycle | 39,626 | count | [Basu et al., J. Road Safety 37(2)](https://journalofroadsafety.org/article/161217-urban-and-rural-differences-in-driver-speeds-and-associated-factors-results-from-a-large-scale-roadside-study-in-india), DOI 10.33492/JRS-D-26-2-2719111 | 2022 data | sourced |
| Urban, sedan/saloon | 33,832 | count | same | 2022 | sourced |
| Urban, SUV | 10,240 | count | same | 2022 | sourced |
| Urban, three-wheeler | 8,859 | count | same | 2022 | sourced |
| Urban, bus | 5,469 | count | same | 2022 | sourced |
| Urban, truck/large truck | 4,593 | count | same | 2022 | sourced |
| Urban, pickup/light truck | 4,360 | count | same | 2022 | sourced |
| Urban, minibus/minivan | 1,479 | count | same | 2022 | sourced |
| Urban, other | 176 | count | same | 2022 | sourced |
| Urban total | 108,634 | count | same | 2022 | sourced |
| Study design | 15 urban + 10 rural sites, May-Oct 2022, 07:30-24:00 in 90-min sessions, handheld radar | - | same | 2022 | sourced |
| Peak-hour passenger-trip share: 2W / car+taxi / auto-IPT / public transport | 24 / 21 / 8 / 48 | % of trips | [CMP Bengaluru, Sec. 2.2](https://dult.karnataka.gov.in/assets/front/pdf/Comprehensive_Mobility_Plan.pdf) | 2015 | sourced (trips, not vehicles) |
| Registered fleet | 74.06 | lakh | CMP Fig. 2-9 (same link) | 2018 | registrations-not-road-share |
| Registered 2W / cars+jeeps share | 69 / 19 | % of fleet | CMP Sec. 2.2.5 | 2018 | registrations-not-road-share |
| Outer-cordon passenger / goods share | 83 / 17 | % | CMP Table 2-17 | 2015 | sourced (cordon only) |
| UVH-26 per-class box counts | - | - | [arXiv 2511.02563](https://arxiv.org/abs/2511.02563), [HF card](https://huggingface.co/datasets/iisc-aim/UVH-26) | 2025 | not-found (card lists 14 classes, 26,646 images, 80/20 split, CC BY 4.0; no per-class counts on card or abstract) |
| City-wide classified count in CMP, IISc/CiSTUP counts | - | - | - | - | not-found |

Derived road-share (urban BMR sites), mapping to simulator classes; "other" (176) dropped, bicycles not counted in the study:
bike = 39,626; auto = 8,859; car = sedan + SUV = 44,072; lcv = pickup + minibus/minivan = 5,839; bus = 5,469; truck = 4,593; sum = 108,458.
Shares = count / 108,458: bike 0.3654, auto 0.0817, car 0.4063, lcv 0.0538, bus 0.0504, truck 0.0424.
Caveat: radar-gun sampling at 25 sites incl. a mix of road types; minivans put in lcv by choice (could be car).

## 2. Hourly variation

| parameter | value | unit | source | year | status |
|-|-|-|-|-|-|
| City morning peak hour | 09:00-10:00 | clock | CMP App. A3.1 (CMP link above) | 2015 | sourced |
| CTTS junction peak hours (Table 2-15) | 09-10, 17-18, 19-20 | clock | CMP Table 2-15 | 2015 | sourced |
| Peak-hour share of 24 h volume, Silk Board | 22,634 / 323,099 = 7.0 | % | CMP Table 2-14 | 2015 | derived |
| Peak-hour share of 24 h volume, Hebbal | 23,924 / 273,755 = 8.7 | % | CMP Table 2-14 | 2015 | derived |
| Other junctions in Table 2-14 | about 5.5-9 | % | CMP Table 2-14 | 2015 | derived (approx, not all computed) |
| TomTom average congestion level | 74.4 | % | [TomTom Traffic Index](https://www.tomtom.com/traffic-index/bengaluru-traffic/) | 2025 | sourced |
| TomTom 10 km travel time, all day / morning rush / evening rush | 36:09 / 41:06 / 45:27 | min:s | same | 2025 | sourced |
| TomTom speed, all day / morning rush / evening rush | 16.6 / 14.6 / 13.2 | km/h | same | 2025 | sourced |
| TomTom weekday 10 km time, overnight / 08:00 / 10-16 h / 18:00 | ~19-20 / ~34-35 / ~40-42 / ~44-46 | min | same (read off grid) | 2025 | sourced (approx) |
| 24 hourly volume fractions | - | - | - | - | not-found |
| Uber Movement, BTP hourly profile | - | - | - | - | not-found (not located; Uber Movement shutdown not verified) |

TomTom gives travel time, not volume, so it must not be used as a volume profile.

## 3. Saturation flow, PCU, capacity

| parameter | value | unit | source | year | status |
|-|-|-|-|-|-|
| Anusha, Verma, Kavitha measured saturation flows, TW proportions, adjustment factor value | - | - | [ASCE JTE 139(5):448-457](https://ascelibrary.org/doi/10.1061/%28ASCE%29TE.1943-5436.0000519), DOI 10.1061/(ASCE)TE.1943-5436.0000519 | 2013 | not-found (paywalled; abstract only) |
| Anusha et al. qualitative result | strong correlation of saturation flow with TW share; new TW factor added to an HCM-based model | - | same | 2013 | sourced (abstract) |
| IRC:106 PCU 2W (5% / 10%+ share) | 0.5 / 0.75 | PCU | [IRC:106-1990 Table 1](https://thelibraryofcivilengineer.files.wordpress.com/2015/09/irc-106-1990-guidelines-for-capacity-of-urban-roads-in-plain-areas.pdf) | 1990 | sourced |
| IRC:106 PCU car | 1.0 / 1.0 | PCU | same | 1990 | sourced |
| IRC:106 PCU auto-rickshaw | 1.2 / 2.0 | PCU | same | 1990 | sourced |
| IRC:106 PCU LCV | 1.4 / 2.0 | PCU | same | 1990 | sourced |
| IRC:106 PCU truck/bus | 2.2 / 3.7 | PCU | same | 1990 | sourced |
| IRC:106 PCU bicycle | 0.4 / 0.5 | PCU | same | 1990 | sourced |
| IRC:106 service volume, 2-lane one-way arterial | 2,400 | PCU/h | same, Table 2 | 1990 | sourced |
| IRC:106 service volume, 6-lane divided arterial | 5,400 | PCU/h | same, Table 2 | 1990 | sourced |
| IRC:106 per-lane equivalents | 1,200 (2-lane one-way: 2400/2); 900 (6-lane: 5400/6) | PCU/h/lane | computed from above | 1990 | derived (service volume, not saturation flow) |
| Indo-HCM PCU 2W / auto / car / LCV / bus / truck | 0.30 / 1.20 / 1.00 / 3.00 / 4.50 / 5.00 | PCU | [course slides citing Indo-HCM](https://www.slideshare.net/slideshow/capacity-level-of-service-highways-signalized-intersections-indohcm/248889022) | 2017 | sourced (secondary; slides label them intermediate/two-lane roads, may not be urban values) |
| Indo-HCM base saturation flow, signal approach, w < 7 m | 630 | PCU/h/m | same slides; same values quoted in [Sushmitha & Ravishankar, IET ITS 2020](https://doi.org/10.1049/iet-its.2019.0470) | 2017 | sourced (secondary) |
| Indo-HCM base saturation flow, 7 <= w <= 10.5 m | 1140 - 60w | PCU/h/m | same | 2017 | sourced (secondary) |
| Indo-HCM base saturation flow, w >= 10.5 m | 500 | PCU/h/m | same | 2017 | sourced (secondary) |
| Primary CRRI Indo-HCM text | - | - | [CRRI snippets](https://crridom.gov.in/sites/default/files/files/Indo-HCM%20Snippets.pdf) | 2017 | not-found (values not extracted from primary) |

## 4. Junction volumes and signal timing

CMP Table 2-14 (Revised Master Plan 2031 draft counts, 2015 base). Column order in the PDF text is ambiguous (PCU is below vehicles at some rows and above at others), so values are as printed.

| junction | peak veh | peak PCU | 24 h veh | 24 h PCU | type | status |
|-|-|-|-|-|-|-|
| Silk Board | 22,634 | 18,180 | 323,099 | 281,521 | 4-leg | sourced |
| Hebbal | 23,924 | 18,154 | 273,755 | 253,689 | 3-leg | sourced |
| Tin Factory | 15,311 | 16,919 | 242,638 | 268,529 | staggered | sourced |
| HSR 27th Main | 15,282 | 12,773 | 172,375 | 149,113 | 3-leg | sourced |
| Nagawara | 14,207 | 11,686 | 167,711 | 153,725 | 4-leg | sourced |
| Hennur Cross | 16,559 | 35,852 | 200,921 | 426,855 | 5-leg | sourced, PDF row looks garbled |
| Doddanakundi | 8,728 | 7,032 | 101,324 | 91,960 | 5-leg | sourced |
| Kundalahalli | 6,280 | 5,656 | 89,599 | 80,770 | 4-leg | sourced |

Link: [CMP](https://dult.karnataka.gov.in/assets/front/pdf/Comprehensive_Mobility_Plan.pdf).
Also in CMP Table 2-15: BEL Circle 18,917 veh / 21,476 PCU (19-20 h); Jalahalli 16,432 / 20,957 (09-10 h); Hoodi 6,600 / 10,035 (17-18 h). 75 CTTS intersections exceed 10,000 PCU in the peak hour.
KR Puram, Marathahalli, Domlur: not-found in the pages read.

| parameter | value | source | status |
|-|-|-|-|
| BTP signal cycle lengths | - | [OpenCity BTP signal timing dataset](https://data.opencity.in/dataset/bengaluru-city-traffic-signal-data) (10 PDFs listed) | not-found (PDFs exist, not opened) |

## 5. Behaviour parameters

| parameter | value | unit | source | year | status |
|-|-|-|-|-|-|
| VISSIM calibrated: standstill distance | 1.00 | m | [Siddharth & Ramadurai, Procedia SBS](https://www.sciencedirect.com/science/article/pii/S1877042813045229) | 2013 | sourced (Chennai Tidal Park, not Bengaluru) |
| same: additive / multiplicative safety distance | 0.20 / 0.78 | - | same | 2013 | sourced (Chennai) |
| same: min lateral distance, bike at 0 km/h | 0.62 | m | same | 2013 | sourced (Chennai) |
| same: min headway | 0.11 | s | same | 2013 | sourced (Chennai) |
| same: look-ahead min / look-back min | 27.91 / 14.31 | m | same | 2013 | sourced (Chennai) |
| same: desired accel bike / HMV at 0 km/h | 6.47 / 4.61 | m/s^2 | same | 2013 | sourced (Chennai) |
| same: validation error | 10.20 / 7.79 | % (two levels) | same | 2013 | sourced |
| Urban BMR observed median speed: all / motorcycle / three-wheeler / sedan / SUV / bus / truck | 46 / 45 / 38 / 50 / 52 / 41 / 44 | km/h | Basu et al. (link in section 1) | 2022 | sourced (radar spot speed, 15 urban sites, off-peak mix incl.) |
| SUMO motorcycle: length 2.0, width 0.8, accel 3.0, decel 5.0, tau 0.5, sigma 0.8, lcSublane 3.62, minGapLat 0.272, latAlignment arbitrary | as stated | SI | ScienceDirect S1389128626005220 (city not verified) | 2026 | sourced (secondary, illustrative only) |
| Mathew & Radhakrishnan 2010 parameter values | - | - | - | 2010 | not-found |
| Maheshwary 2020 parameter values | - | - | - | 2020 | not-found |
| SUMO sublane options (lcSublane, latAlignment, minGapLat) | documented | - | [SUMO docs](https://sumo.dlr.de/docs/Simulation/SublaneModel.html) | - | sourced |
| TomTom rush-hour speed (calibration target) | 13.9 avg; 14.6 morning; 13.2 evening | km/h | TomTom link in section 2 | 2025 | sourced |

## 6. 2012 benchmarks: what they did

| benchmark | what it did | data/validation | what is not known | status |
|-|-|-|-|-|
| (a) Anusha, Verma, Kavitha, ASCE JTE 139(5), received May 2012, online Nov 2012 | Collected saturation flow at a few signalised Bangalore intersections, found strong correlation with TW share, added a TW adjustment factor to an HCM-based model; modified equation fit observed flow better | Field data at Bangalore signals (abstract) | Sites, flows, factor value, method (paywalled) | sourced (abstract) |
| (b) SiMTraM, IIT Bombay (T.V. Mathew), [SourceForge](https://sourceforge.net/projects/simtram/), GPLv3 | Non-lane-based mixed traffic on SUMO 0.12: lane width split into strips, gradual lane change | Screenshots of Powai (Mumbai) network; 2016 redevelopment [Patel et al., Transp. Res. Procedia 17, DOI 10.1016/j.trpro.2016.11.081](https://doi.org/10.1016/j.trpro.2016.11.081) validated on two Ahmedabad stretches (500-5000 veh/h) vs Greater Ahmedabad Mobility Report 2012, mix bike 0.362, cycle 0.032, rickshaw 0.173, car 0.384, HGV 0.05, bus 0.01 | SourceForge registered 2013-02-05, last update 2013-04-29, latest SiMTraM-0.1.1; the "v0.1.0 June 2012" date was not confirmed. Not Bengaluru. Known segfaults on large networks | sourced |
| (c) Other ~2012 IISc simulation of heterogeneous Bengaluru traffic | - | - | - | not-found |

## Recommended defaults for the simulator

**modal_split** (status: derived from the 2022 urban BMR roadside counts, section 1; replace if UVH-26 per-class counts are obtained). Bicycles are excluded.

| class | share |
|-|-|
| bike | 0.365 |
| auto | 0.082 |
| car | 0.406 |
| lcv | 0.054 |
| bus | 0.050 |
| truck | 0.043 |
| sum | 1.000 (rounded; unrounded shares sum to exactly 1) |

Mapping: car = sedan + SUV; lcv = pickup + minibus/minivan; "other" dropped. Registration shares (2W 69%, car 19%) are not road share and should not be used for flow generation.

**hourly_profile** (status: not-found). No source gives 24 hourly volume fractions for Bengaluru. Sourced anchors only: morning peak 09:00-10:00 (CMP), further junction peaks 17-18 and 19-20 (CMP Table 2-15), peak hour = about 7.0-8.7% of daily volume at Silk Board and Hebbal (derived). A 24-value vector would have to be an explicit assumption; do not cite it as sourced. TomTom travel-time curve is context only.

**saturation flow per lane for validation** (status: derived and secondary):
- Indo-HCM signal base saturation flow: 630 PCU/h/m for approach width under 7 m, so a 3.5 m lane is 630 x 3.5 = 2,205 PCU/h/lane (derived, secondary source). Use as an upper-bound target, not a Bengaluru measurement.
- IRC:106 service volumes imply about 900-1,200 PCU/h/lane (derived); these are design service volumes, lower than saturation flow.
- Anusha et al. Bangalore measured values: not-found.

**PCU factors**:
- IRC:106-1990 (sourced, primary, 10%+ share column): 2W 0.75, car 1.0, auto 2.0, LCV 2.0, truck/bus 3.7, bicycle 0.5. The 5% column is 0.5, 1.0, 1.2, 1.4, 2.2, 0.4.
- Indo-HCM (sourced, secondary, slide values, possibly the intermediate/two-lane table): 2W 0.30, auto 1.20, car 1.00, LCV 3.00, bus 4.50, truck 5.00.
- Pick one set and state it; the two disagree most for 2W (0.30 vs 0.5-0.75) and LCV.

## Open gaps worth closing

1. UVH-26 per-class box counts (download the dataset annotations and count; CC BY 4.0).
2. Hourly volumes: BTP/ITMS counts or ATCC data; none found open.
3. Anusha et al. 2013 full text (institutional access).
4. BTP signal PDFs on OpenCity for cycle lengths.
5. Primary Indo-HCM tables for urban PCU values.
