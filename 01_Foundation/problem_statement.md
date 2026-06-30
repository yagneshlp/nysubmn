# 01 — Problem Statement (Foundation)

*Synthesis of the provided brief, data dictionary, pricing log, and AI analysis.
This is our shared context of record. Status: DRAFT for user review.*

---

## The leadership prompt (the thing we're reacting to)
> "Completed auto rides per day in Bangalore have gone nowhere this quarter — they slipped
> through May — but since we shipped congestion-based pricing two weeks ago they've ticked
> back up, so we think it's working. **Grow completed rides.**"

Driver-ops wants to roll `250/252` to 100% of Bangalore autos, then to other cities.
**Our job across the brief: pressure-test that belief before the ship decision.**

## What makes Namma Yatri structurally different (the constraints we reason within)
- **Zero commission.** Drivers pay a small flat subscription; NY takes nothing per fare.
  Competitors went zero-commission too, but fund bonuses by **burning investor money. NY won't.**
  → **The only pricing lever on a trip is the rider's fare. No subsidy. Every rupee must pay for itself.**
- **Moat is structural, not financial:** decade of tech (open Beckn/ONDC stack, in-house
  pricing/matching → lowest cost to serve) + community/public-good trust. Compete on
  **cost, tech, trust — not out-spending.**
- **Stale government tariff.** Distance-only meter, almost no time-of-day component
  (9am peak and 2pm empty-road priced the same). At peak the fare can sit **below the
  driver's real cost** → driver doesn't quote. This is the gap congestion pricing targets.
- **Genuine two-sided marketplace.** Riders search; drivers *independently choose* whether
  to quote and whether to honour a booking, and **multi-home** (drive for competitors).
  Neither side is captive.
- **Driver's unit is earnings/hour, not per trip.** The **deadhead pickup** (unpaid time +
  fuel to reach the rider) is a hidden cost that kills short, low-fare trips.
- **NY never observes a whole class of trips.** A rider who gets no/expensive quote silently
  opens another app. **That lost demand isn't in the tables.**

## The intervention under test
A **congestion charge**: when an area is busy (real-time demand/supply "QAR" signal), the
rider's fare is multiplied up a bit so a skipped trip becomes worth a driver's while —
funded by the rider, not a subsidy. Rider fare ≈ (base + extra-km) × congestion multiplier.
**Rupee reality check:** a 1.15× on a 5 km ride (₹75 meter) adds only ~₹11. The lever is small;
do the math before assuming it's large.

## The pricing versions (this was NOT one clean experiment)
| ver | window | share | avg cong. | what it was |
|----|--------|------|-----------|-------------|
| 211 | May 18–Jun 2 | ~13% | ~1.04 | acceptance-first, near-zero auto surge, lowest fares |
| 234 | May 18–Jun 4 | ~15% | ~1.16 (Pri ≈1.49) | high congestion, aggressive surge |
| 236 | May 18–Jun 22 | ~35% | ~1.12 | long-standing **baseline** (moderate), live whole window |
| 239–248 | Jun 4–10 | ~12% | 1.02–1.19 | rapid A/B burst, each live ~1–5 days |
| 250 | Jun 10–Jun 22 | ~17% | ~1.11 | **current rollout**, being ramped |
| 252 | Jun 15–Jun 22 | ~7% | ~1.11 (Pri ≈1.41) | latest, stronger add-on esp. Auto Priority |
- Two arms: **congestion-up** (234, 236, 250, 252) vs **acceptance-first** (211, 245, 247, 248).

## Confounds we must respect (or the analysis is worthless)
- **Assignment is observational** — varies by zone, time-of-day, gradual ramp. Not random.
- **Outcome-dependent rollout** — winners ramped toward 100% (a version at 100% has no control left).
- **Time-of-day gating:** `250/252` run mainly in **peak** (~08–11, 16–20); baseline `236` runs
  mainly **off-peak/midday/night**. Overlap only in morning shoulder (~08–10) & midday;
  **evening peak has essentially no 236.** → Naive `236 vs 250` = **off-peak vs peak**, not a
  pricing test. **The one clean head-to-head is `250 vs 252` inside peak.**
- **Distance is NOT confounded** — every version appears across all distance bands similarly.

## The data (scope: Bangalore autos, 2026-05-18 → 06-22)
- `data/rides.csv` — funnel cube, **25,280 cells**. Funnel order:
  `searches (+retries) → rider_acceptances → rides (bookings) → completed | cancelled`
  (`_by_driver` / `_by_user` / `_other`). Driver behaviour shows up via `cancelled_by_driver`.
  Key rates: completion = completed/searches · cancel = cancelled/rides ·
  driver-cancel share = cancelled_by_driver/cancelled · avg fare = completed_fare_sum/completed ·
  avg congestion = congestion_sum/congestion_n.
- `data/competitor_fares.csv` — fare cube, **17,785 cells**, `competitor ∈ {competitor1,
  competitor2, namma_yatri}`, with `n` = sample size. Routes skew long (~16 km median) →
  compare within `distance_bucket` or via `price_per_km_p50`.
- **Base meter:** Auto ₹30 base (incl. 2 km) + ₹15/km; Auto Priority ₹36 + ₹18/km. No time charge.

## What the data CANNOT tell us (matters for Part 5)
No per-rider/per-driver behaviour (no ids → no repeat-rider, no earnings/hour), no geo/zone,
no per-trip fare beyond quantiles, no ratings, no weather, and **no record of riders who got
no quote and silently left.**

## The AI analysis we must stress-test (Part 5)
Claims: rollout (v250/252, "rolled out 2026-06-10") lifted completed rides **+14.9%** via
completion-per-search (0.496→0.569), fares ~flat (+1.5%), cancellations flat, Auto Priority
"loves it" (0.77–0.85). Recommends **immediate 100% rollout + Delhi/Kolkata expansion.**
→ Built on a naive all-auto before/after across the exact off-peak-vs-peak confound above.
This is the central thing we suspect is wrong.

## Our north star for the engagement
Separate **"completed rides went up"** from **"congestion pricing *caused* it, in a way that's
win-win and worth shipping."** Specifics over averages. Slices over "autos overall."
