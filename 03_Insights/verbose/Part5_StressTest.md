# Part 5 — Stress Test the AI Analysis

> *Four things the attached analysis gets wrong, overstates, or quietly assumes, each tied to the
> ship decision; then what this dataset cannot tell us about why completed rides are flat, and how I
> would get the signal.*

The analysis is not wrong because it computed badly. It computed one number correctly and then asked
that number to carry a decision it cannot bear. I reproduced its headline exactly: all-auto
completion-per-search did rise from 0.496 to 0.569 across the rollout, +14.9% to the decimal. That is
the moment to push past the AI rather than nod along, because the number survives recomputation and
still fails as evidence. Everything below is why a correct calculation produces a wrong recommendation.

## Critique 1 — The headline is a confound wearing a causal claim

The method compares "before (May 18–Jun 9) versus after (Jun 10–Jun 22) across all Bangalore auto
transactions." That single sentence contains the whole error, because the versions were never assigned
cleanly: v250 and v252 run mainly in peak hours, while the v236 baseline runs mainly off-peak and at
night. So a plain before-and-after is not pricing against no-pricing; it is peak against off-peak, and
this month's demand against last month's. Three checks dismantle the +14.9%. The lift appears just as
strongly in the no-surge hours, where Auto completion rose from 0.335 to 0.437 at night and 0.430 to
0.522 off-peak, and a lever that only fires at peak cannot move hours where it never fired. The ratio's
denominator fell, with Auto searches dropping from 181,000 a day to 168,000, so completion-per-search
climbed partly because fewer people were asking. And the raw count of finished rides, the metric
leadership actually cares about, shows the Auto recovery beginning *before* the rollout, 82,900 a day in
late May to 88,900 in early June, with the post-rollout window adding only the last leg on a shrinking
base. **Ship implication:** the number that anchors the entire recommendation is not measuring the
pricing. The one clean comparison the rollout left behind, v250 against v252 inside the same peak hours,
shows a real effect that is far narrower and tier-specific, which is the opposite of a green light for a
blanket rollout.

## Critique 2 — The asserted mechanism is absent, and the analysis contradicts itself

Finding 5 states the causal story plainly: "congestion pricing increases driver supply, which is why
completion improved." On the mass Auto tier that mechanism is physically absent. The applied congestion
multiplier moved from 1.062 to 1.068, about six rupees on a ₹150 fare, and a six-rupee nudge does not
summon a supply wave. Worse, the analysis contradicts itself: Finding 2 celebrates that "average fare
barely moved (+1.5%)," but if the fare barely moved then the charge barely applied, and a charge that
barely applied cannot be the thing that raised supply. The two findings cannot both be true as told. And
the analysis makes a falsifiable prediction, that the logic "should help most on longer trips," which the
data rejects: the clean dose-response runs *inverse* on Auto, where bands with more surge show less
completion, not more, and the only genuine dose-response, on Auto Priority, concentrates in short and mid
bands while the long bands it predicted show no lift at all. **Ship implication:** a 100% rollout to the
mass tier is a bet on a causal channel the data denies. If the surge is not moving supply on Auto, then
scaling the surge on Auto scales a placebo, and the real leak, cancellation over the deadhead, stays
exactly where it was.

## Critique 3 — "Auto Priority loves it" mistakes a ratio for rides and supply for sentiment

The analysis calls Auto Priority "excellent," reading 0.77–0.85 completion-per-search as proof that
"riders love congestion pricing." Two things are wrong. First, it confuses a ratio with a count. Auto
Priority's completed rides per day actually *fell* after the rollout, from about 16,900 to 15,900, the
lowest of the window, even as the ratio rose, because its search denominator collapsed from 25,400 a day
to 20,800. The tier the analysis leans on hardest delivered fewer finished rides, which is the precise
opposite of the brief's goal of growing completed rides. Second, completion-per-search is a marketplace
clearing rate, not a satisfaction signal; it says nothing about whether riders "love" anything, and it
structurally cannot see the riders who got no usable quote and silently left, who are the ones a price
increase would push away first. **Ship implication:** the single strongest piece of evidence in the
analysis points the wrong way once you count rides instead of ratios. Crowning the premium tier the
winner while its absolute volume shrinks is how you ship a number that looks like growth and ship away
the growth itself.

## Critique 4 — "Proven at scale, ready for 100%" turns the rollout's bias into its proof

The conclusion argues that "v250 now serves the large majority of auto volume, so the effect is proven at
scale." This inverts a confound into a credential. Winning versions were ramped toward 100% precisely
because they looked good, so v250's large share is the *consequence* of the selection, not independent
proof of its effect; a version sitting near 100% has no control group left to compare against, which is
why "proven at scale" is circular rather than reassuring. The flat cancellation rate (0.315 to 0.311) is
read the same hopeful way, as evidence the gains were clean, when on a marketplace whose biggest leak is
cancellation a *flat* cancellation rate means the intervention did nothing for the one thing that matters
most, and a pooled rate can hide a driver-to-rider attribution shift if drivers stall to force the rider
to cancel. Then the recommendation leaps to "start the Delhi/Kolkata rollout this sprint," with zero
evidence from any city but Bangalore, whose stale tariff, supply density, and competitive intensity are
exactly the variables that would not transfer. **Ship implication:** every safeguard that should slow a
rollout, an absent control, a flat cancellation rate, an untested geography, is reframed here as a reason
to go faster. That is the most dangerous error in the document, because it is a process error, and a
process that treats its own selection bias as proof will keep shipping until something breaks.

## What this dataset cannot tell us about why completed rides are flat

The honest limit is that this cube can describe the trips Namma Yatri served and almost nothing about the
trips and people it lost, which is where the answer to "why are rides flat" actually lives. Five gaps
matter, and each has a way to close it.

The first and largest is the **silent no-quote**. The data dictionary is explicit that a rider who got no
usable quote and left for another app is not in the funnel, and the fare columns are measured on completed
rides only, so we cannot see the price a non-converting rider was shown or why she left. To get it, I
would instrument the search itself: log every search as quote-shown, no-quote, or quote-rejected, attach
a reason and the quoted fare to each, and run periodic exit prompts on abandoned searches. That single
change would convert the most important failure in the marketplace from invisible to measured.

Second, there are **no rider or driver ids**, so there is no retention, no repeat-rider cohort, and no
earnings-per-hour, which is the exact number the driver in Part 3 optimizes. A privacy-safe persistent id
would let us see whether flat completed rides come from the same riders riding less or from churn, and
whether drivers are earning enough per hour to stay online.

Third, there is **no geography**. We cannot see pickup distance, the deadhead that drives cancellation,
or the zone-level mismatch between where supply sits and where demand forms, which is the very signal the
Part 4 supply-shaping lever needs. Capturing pickup distance and zone-level supply and demand is the
prerequisite for both diagnosing the leak and fixing it.

Fourth, there is **no view of the driver's outside option**. The competitor file shows rider-facing
fares, but under a commission-and-subsidy rival the driver's payout is decoupled from that fare, so the
poach that pulls a driver off a Namma Yatri booking is unobservable. A driver multi-homing panel and a
scrape of competitor driver incentives would expose it.

Fifth, there are **no exogenous controls**: no weather, no exam or holiday calendar, no record of when a
competitor opened or closed its subsidy tap, any of which can swing completed rides for two weeks and land
in the rollout window by coincidence. Merging weather, calendar, and competitor-event data lets us subtract
the noise the analysis currently credits to the pricing.

The deepest fix underneath all five is the one the rollout never had: a **real randomized holdout**.
Because assignment was observational and outcome-dependent, no amount of clever slicing fully separates
the pricing from the confounds. A small, deliberately held-back control, randomized within zone and hour,
would answer in two weeks what this entire dataset cannot answer at all, and it is the one thing I would
insist on before any city-wide ship.
