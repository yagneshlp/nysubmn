# 02 — Sanity-Check Findings (grounding for Part 1)

*Source: `01_sanity_check.py`, `02_decompose_confound.py`. Additive cols only; no median averaged.*

## Headline: we reproduced the AI's number exactly, then took it apart
- Naive all-auto completion/search: **0.496 → 0.569 = +14.9%** (matches AI's claim to the decimal).
- That number does **not** survive contact with the data as a pricing effect.

## What the data actually says

**F1 — The surge dial barely moved for the mass tier, yet completion "jumped."**
Weighted avg congestion actually applied to **Auto: 1.062 → 1.068** (PRE→POST) — a rounding
error (~₹6 on a ₹150 fare). The AI's asserted mechanism (more surge → more supply → more
completion) is **physically absent** in the Auto data. A 0.6% fare nudge cannot drive a 15%
completion lift. → *Whatever moved completion, it largely wasn't the congestion charge.*

**F2 — The lift is broad-based, including off-peak where surge ≈ 1.0.**
Holding tier + time-of-day fixed, completion/search still rose: Auto peak +19%, **off-peak +10%**,
night +16%. It improved *everywhere*, including hours with essentially no surge. A lever that
only acts at congested peaks cannot explain an off-peak gain. → points to a **system-wide**
cause (supply, matching, seasonality, demand cooling) — not pricing.

**F3 — The "lift" is mostly a shrinking denominator, not more rides.**
Searches/day **fell** post-rollout: peak −10%, night −17%. Completion/search is a ratio; a
smaller denominator inflates it. The metric leadership actually cares about — **completed
rides/day** — moved far less: **Auto ~89k(Jun1-9) → ~92k(Jun10-22), only +3%**, and was already
recovered before rollout. **Auto Priority completed/day FELL** (16.9k → 15.9k), its lowest of
the window — despite the AI calling Priority the big winner on its 0.77–0.85 *ratio*.

**F4 — My own framing was wrong, and I corrected it (prompt-trail flag).**
I expected the +14.9% to be a pure peak/off-peak Simpson's mix-shift. **It isn't** — search-share
by ToD barely moved (63%→62%) and the lift persists within each bucket. The real confounds are
(a) the falling denominator [F3] and (b) the broad-based, surge-independent lift [F2]. I updated
the hypothesis to match the data instead of the data to match the hypothesis.

**F5 — The brief's "evening peak has no 236" is only true POST-rollout.**
Evening-peak (16–20) Auto version mix: May18-31 was **v236 49% + v234 48%** (234 = aggressive
surge); Jun10-22 is **v250 67% + v252 27%**. So a before/after in evening peak compares
*surge-config-A vs surge-config-B* — **not** "no pricing → pricing." The PRE side was already surged.

**F6 — The clean comparison (250 vs 252 inside peak) is the only honest pricing read.**
- *Auto:* 252 completion 0.513 vs 250 0.480; but 252's fare is **lower** (152 vs 154) and congestion
  ~equal (1.07). The small edge isn't coming from *more* surge.
- *Auto Priority:* 252 completion 0.841 vs 0.764, with higher congestion (1.42 vs 1.36) and higher
  fare (186 vs 180) — here more surge *does* track higher completion, but absolute Priority volume is flat/down.
  → Defection check (competitor_fares) still required before crediting it.

**F7 — The real leak is cancellation, not search-to-quote.**
Funnel: Auto rides→completed loses **31% to cancellation**, driver-cancel share **~0.52**. The
cancellation leak dwarfs the ~₹6 surge nudge as a lever on completed rides.

## Implication for framing
The question isn't "did completion/search rise" (it did, as a ratio). It's "did **completed
rides** grow *because of congestion pricing*." On the mass tier the surge barely moved, the gain
appears in no-surge hours too, and the denominator fell — so the honest prior is **mostly not
the pricing**. The big untouched lever is **cancellation**.
