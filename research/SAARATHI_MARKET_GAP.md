# Saarathi: Market Gap (short)

2026-11-16. Desk research only (web and news search, a few page reads). Not primary research. No customer interviews, and no tender text was read in full (two tender PDFs failed to load). Everything below is a hypothesis to test, not a finding.

## What exists
- **Deployed adaptive systems:** Bengaluru's BATCS had 103 adaptive junctions in early 2025, aiming for 165 (Bangalore Mirror, Feb 2025). Other Indian cities (for example Gurugram/GMDA) have ATCS tenders, but I could not load the tender documents, so their performance and validation terms are unchecked.
- **Vendors:** Indian vendors (for example Krypton AI) sell "built for mixed, non-lane traffic" ATCS. Their own guide lists "simulation of signal changes before go-live" and "before/after audit reports" as things a city should ask for (kryptonai.in, Oct 2026). Global tools such as Flow Labs sell "predict a new timing plan before implementation" as a closed commercial module.
- **Evidence of independent checks:** I found no published independent performance numbers. The BATCS press coverage I read (Bangalore Mirror) reports none and mentions no validation. My search for audit findings returned nothing, which is not proof that none exist.

## The gap (hypothesis)
Cities buy adaptive signals on vendor claims and there is **no open, neutral way to test a vendor's algorithm on your own junction with Indian traffic before paying**. Vendors say "built for India" but publish no benchmark. Commercial simulators (VISSIM, Aimsun) are closed, expensive and lane-based by default. Open research benchmarks (RESCO, LibSignal) assume lane-disciplined traffic. Nandakumar et al. (*preprint*) covers one junction only.

So the open slot is **neutral, open, pre-deployment and post-deployment evaluation for Indian mixed traffic**, not "a better controller".

## Who would use it (unvalidated)
| User | Why | Pays? |
|---|---|---|
| City/traffic police engineers, smart-city cells | Check vendor claims, compare against current fixed plan | Unlikely to pay for software; may pay for a study |
| Consultants (tender writers, third-party auditors) | Need a defensible, repeatable test protocol | Possible |
| Researchers, students | Benchmark to publish against | No; this is the adoption driver |
| Vendors | A credible leaderboard to show | Possible, but a conflict of interest |

## What this means for Saarathi
1. **Positioning:** "open evaluation layer", as `PART_A_COMPLETION.md` §4 already says. Part B's controller is a demo, not the product.
2. **Features worth more than another RL method:**
   - sensing-tier curve (works with cities' existing CCTV: what do you lose with counts only?)
   - worst-seed / reliability reporting (the thing audits care about)
   - junction report card (before/after KPIs in audit language)
   - own-plan baseline (race a vendor against the city's real signal plan)
3. **Credibility gap:** none of this is trusted without field-calibrated validation (A2/A3). That is the blocker for both the paper and any real user.

## Risks
- Cities may not care about open tools; procurement is relationship-driven (untested).
- Vendors have no incentive to be benchmarked.
- A competing open benchmark could appear (the IIT Madras group lists our gaps as future work).

## Cheapest validation (before building more)
Talk to 5 people: 2 traffic police/ATCS cell engineers, 1 smart-city consultant, 1 vendor engineer, 1 professor from the IIT Madras / IISc traffic group. Ask: "How do you check a vendor's claim today? What would you need to trust a simulation?" If most say "we don't", the gap is real.
## Not claimed
No market size, no willingness-to-pay, no claim that BATCS is bad. The vendor claims are unverified.
