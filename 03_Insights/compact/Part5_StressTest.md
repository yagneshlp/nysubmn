# Part 5 — Stress Test the AI Analysis

The analysis computed one number correctly and then asked it to carry a decision it cannot bear. I reproduced the +14.9% headline exactly, to the decimal, so there is no hiding behind a computation dispute. What follows is why a correct calculation produces a wrong recommendation.

## Critique 1 — The headline is a confound wearing a causal claim

The method compares all Bangalore auto transactions before vs after the rollout. The versions were never cleanly assigned: v250/252 run mainly at peak; v236 runs mainly off-peak and at night. A before-and-after is peak vs off-peak, not pricing vs no-pricing.

Three checks dismantle the +14.9%:
- The lift appears equally at night (Auto: 0.335 → 0.437) and off-peak (0.430 → 0.522), where the charge never fired. A lever that only acts at peak cannot move hours it never touched.
- The denominator fell: Auto searches dropped from 181k to 168k per day. Completion-per-search climbed partly because fewer people were asking.
- Raw Auto completed rides began recovering before the charge shipped: 82,900/day in late May to 88,900 in early June.

**Ship implication:** the number anchoring the recommendation is not measuring the pricing. The one clean comparison the rollout left behind (v250 vs v252 at peak) shows a narrower, tier-specific effect, which is the opposite of a green light for a blanket rollout.

## Critique 2 — The asserted mechanism is absent, and the analysis contradicts itself

Finding 5 of the analysis states the causal story: "congestion pricing increases driver supply, which is why completion improved." On the mass Auto tier that mechanism is physically absent. The applied multiplier moved from 1.062 to 1.068, about ₹6 on a ₹150 fare. Finding 2 then celebrates that "average fare barely moved (+1.5%)." These two findings cannot both be true: a fare that barely moved cannot have raised supply. The analysis also predicts the effect "should help most on longer trips," which the data rejects: the only genuine dose-response concentrates on short and mid bands, while the long bands it predicted show no lift at all.

**Ship implication:** a 100% Auto rollout bets on a causal channel the data denies. Scaling the surge on the mass tier scales a placebo, and the real leak, cancellation over the deadhead, stays exactly where it is.

## Critique 3 — "Auto Priority loves it" mistakes a ratio for rides

The analysis reads 0.77–0.85 completion-per-search on Auto Priority as proof "riders love congestion pricing." Auto Priority's completed rides per day actually fell after the rollout, from ~16,900 to ~15,900, because its search denominator collapsed from 25,400 to 20,800. The tier the analysis leans on hardest delivered fewer finished rides. Completion-per-search is also a marketplace clearing rate, not a satisfaction signal; it structurally cannot see the riders who got no usable quote and silently left, who are the ones a price increase would push away first.

**Ship implication:** the single strongest piece of evidence in the analysis points the wrong way when you count rides instead of ratios. Crowning the premium tier the winner while its absolute volume shrinks is how you ship a number that looks like growth and ship away the growth itself.

## Critique 4 — "Proven at scale" inverts selection bias into a credential

The conclusion argues v250's large majority share proves the effect at scale. This inverts the logic: winning versions were ramped precisely because they looked good, so v250's share is the consequence of selection, not independent proof of its effect. The flat cancellation rate (0.315 → 0.311) is read as a clean win; on a platform whose biggest leak is cancellation, a flat rate means the intervention did nothing for the one thing that matters most, and a pooled rate can hide attribution gaming if drivers stall to force the rider to cancel. The recommendation then leaps to "start the Delhi/Kolkata rollout this sprint," with zero evidence from any city but Bangalore.

**Ship implication:** every safeguard that should slow a rollout (absent control group, flat cancellation, untested geography) is reframed as a reason to go faster. A process that treats its own selection bias as proof will keep shipping until something breaks.

## What the dataset cannot tell us

The cube describes trips NY served. The answer to "why are rides flat" lives in the trips and people it lost. Five gaps matter, each with a way to close it:

- **Silent no-quote.** A rider who got no usable quote and left for another app is not in the funnel. Fix: log every search as quote-shown, no-quote, or quote-rejected, with the quoted fare attached.
- **No ids.** No retention, no repeat-rider cohort, no earnings-per-hour (the exact number the driver in Part 3 optimises). Fix: privacy-safe persistent ids.
- **No geography.** No pickup distance, no zone-level supply-demand mismatch; the Part 4 supply-shaping lever has no signal to run on without this. Fix: log pickup distance, tag zones.
- **No view of the driver's outside option.** Competitor rider fares are visible; competitor driver payouts are not. Fix: driver multi-homing panel and competitor incentive scrape.
- **No exogenous controls.** Weather, exam calendar, competitor subsidy events can swing rides for two weeks and land in the rollout window by coincidence. Fix: merge and subtract.

The deepest fix is the one the rollout never had: a real randomized holdout. Because assignment was observational and outcome-dependent, no amount of clever slicing fully separates the pricing from the confounds. A small held-back control, randomized within zone and hour, would answer in two weeks what this entire dataset cannot answer at all. It is the one thing I would insist on before any city-wide ship.
