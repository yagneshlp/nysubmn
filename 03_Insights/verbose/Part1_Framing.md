# Part 1 — Frame the Problem (before the data)

> **Status: PARKED.** Drafted and refined. Coming back to it after Parts 2–5 are done.
> Incorporates the multi-homing / single-dispatch refinement (decision D-009).

*First-principles reasoning plus the experiment log. No ride data opened.*

Leadership has a clean story. Completed rides slipped through May, ticked back up in the two weeks
after congestion pricing shipped, so the pricing must be working, so grow it. The trouble is that
completed rides are not a dial you can turn. A finished ride is the last survivor of a long chain,
and the rider can fall off at any link in it. So the only honest way to reason about the number is
to break it into that chain. Every finished ride is fully accounted for by four multiplied stages,
which means nothing can move finished rides without moving one of these terms.

<figure class="funnel">
  <div class="funnel-out">completed rides <span class="funnel-eq">=</span></div>
  <div class="funnel-chain">
    <div class="stagebox"><span class="stage-k">Stage 0</span><span class="stage-f">searches</span><span class="stage-d">demand volume</span></div>
    <span class="op">&times;</span>
    <div class="stagebox price"><span class="stage-k">Stage 1 <span class="price-tag">price &minus;</span></span><span class="stage-f">acc / search</span><span class="stage-d">rider gets a usable quote &amp; accepts</span></div>
    <span class="op">&times;</span>
    <div class="stagebox hit"><span class="stage-k">Stage 2 <span class="hit-tag">price +</span></span><span class="stage-f">ride / acc</span><span class="stage-d">a driver quotes &amp; matches</span></div>
    <span class="op">&times;</span>
    <div class="stagebox"><span class="stage-k">Stage 3</span><span class="stage-f">1 &minus; cancel</span><span class="stage-d">booking is honoured</span></div>
  </div>
  <figcaption>Amber is the one link the congestion charge is built to move, pulling a driver into Stage 2. The same charge pushes the other way at Stage 1, where a higher fare can send a price-sensitive rider to a cheaper competitor. One lever, two signs, two stages.</figcaption>
</figure>

One honesty note on the arithmetic before I lean on it. This is a decomposition, not four independent
dials: the middle terms telescope, so the identity holds by construction no matter what the numbers
turn out to be. And Stage 1 in particular is not a clean conversion rate. Retries let one search throw
off more than one acceptance, so acceptances can run above searches and this term can sit above 1; it
is a flow ratio, not a probability bounded at 1. I keep it in the chain because it still localizes
where rider-side behaviour shows up, but I expect the real measured leaks to live at Stage 2, rides
per acceptance, and Stage 3, cancellation, and that is where I expect the binding constraint to sit.

I rank my hypotheses by stage, which is what keeps them clean and non-overlapping: each one names
the thing that binds at exactly one stage, and the four stages plus the outside forces cover the
whole space. A congestion charge is not a general lever across this chain. It is a two-signed force
that lives in two specific spots. It raises the fare to pull a driver into Stage 2, and the very
same raise can push a price-sensitive rider out of Stage 1. That is why I split the price story
across two hypotheses below instead of letting it float as one.

## 1. Ranked hypotheses — what drives completed auto rides

**H1 — Stage 3, driver honour. The driver says yes, then bails. [Most likely]**
This is the biggest and the last leak, and it is the one I would bet on first. The finished ride is
the only event that actually pays the driver, and it is also the easiest one for him to walk away
from. He is not thinking about the fare on this one trip. He is thinking about what he earns across
the whole hour, and a long unpaid drive to the pickup quietly wrecks that number. A ₹67 fare with a
1.5 km pickup is not a ₹67 trip to him. It costs him fuel and ten minutes he could have spent
waiting for something better, so the real rate drops below the meter.

When he bails, it happens one of two ways, and the split matters. Either a competitor put a concrete
better trip in front of him, or nothing did and he just dropped a losing trip to go back to waiting.
The first kind is always a competitor, and that is not a coincidence. NY hands a driver one ride at
a time and will not ping him a second while he is assigned, so there is never a rival NY trip
sitting in front of him to jump to. Only Uber or Ola, who cannot see he is busy on NY, can show him
a real alternative while he is holding your booking. Multi-homing is the hole in that wall.

Can price fix this? Barely, and for two reasons. The bump is tiny, and ₹8 does not change a driver's
mind about a genuinely bad trip. And even a large bump cannot win the poach, because the competitor
funds its better offer by burning investor money while NY funds its bump from a small rider charge.
You cannot outbid a subsidy when you take nothing from the fare. So price reaches the biggest leak
in the funnel weakly on the refusal half and barely at all on the poach half. (Stage 3 also hides a
gaming trick, where a driver accepts and stalls to make the rider cancel, which shifts the blame
from his column to the rider's without changing anything real. More on that in Part 3.)

**H2 — Stage 0, demand volume. There is a ceiling, and demand sets it. [High]**
You cannot finish more rides than people ask for, and that cap sits above everything downstream. The
catch is that NY only ever sees the searches it managed to serve. Demand moves with competitor
subsidies, with riders and drivers splitting across apps, with paydays and the exam calendar, and
finished rides move with it no matter how well the funnel is tuned. I put it second rather than
first because it is mostly outside our control. It bounds the number, but product has fewer real
levers on it than it has on cancellation.

**H3 — Stage 2, getting the driver to quote. This is the job congestion pricing is actually built for. [Medium; the lever under test]**
This is the stage the whole exercise is about. Bangalore's meter runs on an old government tariff
that barely moves with the time of day, so at a busy peak the fare can sit below what the trip costs
the driver, and he simply never quotes. A congestion bump is aimed right at that gap. It lifts the
fare on the trips drivers skip until they are worth taking. If it works, it should show up where the
gap actually is, on short trips, at peak, in genuinely busy areas, and stay close to invisible
everywhere else. The rupee math keeps it modest: a 1.1x on a ₹75 ride is about ₹8, which matters at
the exact margin of a skipped trip and disappears in the average.

**H4 — Stage 1, the rider's side. The bad quote, the missing quote, and the same price pushing the other way. [Medium; the invisible one]**
Stage 1 holds two failures the supply hypotheses skip straight over. First, the rider searches and
gets no usable quote at all, because nobody is online to take it. That is a supply-thinness problem,
not a demand problem, and it never shows up as a loss anywhere in the data. Second, the rider gets a
quote and walks because the fare or the wait is too high. This is the exact spot where the
congestion bump cuts the other way: the same ₹8 that nudges a driver to take the trip can be the ₹8
that sends a price-sensitive rider to Uber. I rank it in the middle because it is real and
load-bearing, and I flag it as the most dangerous gap because the missing-quote case is invisible to
every table we have.

**H5 — Everything else moving at once: weather, the calendar, and how hard competitors are spending this week. [Low base rate, high variance]**
These move the inputs to every stage at the same time and have nothing to do with our pricing. June
weather, exams and holidays, a competitor opening or closing the subsidy tap; any one of them can
swing the number for two weeks, and that swing can land in the exact window leadership has pinned on
the rollout. I rank it last on base rate but flag the variance, because it is the single most likely
thing to be quietly doing the work the pricing is getting credit for. (Multi-homing used to live
here in an earlier draft. It does not belong here, because it is a permanent structural feature of
the market, not a passing wind, so it now sits inside H1 where it actually acts.)

## 2. How I would tell cause from coincidence

The rollout was never a clean A/B test, and that one fact drains most of the comfort out of the
before-and-after. Versions were assigned by zone and time of day, and any version that looked good
got ramped toward 100% fast. So a plain before-versus-after is not pricing against no-pricing. It is
peak against off-peak, and last month's demand against this month's. I would only believe the
pricing caused the lift after a slice passes five tests, in order.

The first test asks whether the price even moved. I rebuild the applied congestion multiplier for
the exact slice from congestion_sum over congestion_n, and if the surge never rose, I stop right
there, because pricing cannot cause an effect it never produced. The second test demands a
like-for-like comparison: same tier, distance band, and hour, against the identical slice a week
earlier, so the confounds are held still instead of averaged away. The third test uses the one clean
window the rollout left behind, versions 250 and 252 running side by side inside the same peak
hours, where the time of day is matched and the pricing logic is the only thing left varying. The
fourth test wants dose-response and a placebo together: completion should rise more where the surge
rose more, and stay flat where the price never moved. The fifth test looks past the headline ratio
at the denominator and at both exits. Completion-per-search can climb simply because searches fell,
so I track the raw count of finished rides, not the ratio. And I check NY's fare against competitor1
and competitor2 on both sides at once: high enough to send riders away at Stage 1, or low enough on
the driver's side that the competitor is out-bidding us and poaching the driver off the trip at
Stage 3. The competitor comparison guards both ends of the market, which is exactly why it is a test
and not a footnote.

Two second-order effects make these tests harder, and I would design around them rather than trust
the raw result. Surge in one place pulls drivers online, and those drivers then shorten pickups and
finish more trips nearby and in the shoulder hours, so a flat-looking off-peak placebo can be
contaminated by spillover from the peak next door. The placebo therefore has to sit far from any
surge in both time and zone, not merely off-peak. And surge changes which trips finish, filtering
short unprofitable ones out and longer ones in, so I read completion only within a fixed distance
band and never pooled. Convincing evidence is the slice that clears all five tests with those two
corrections applied. Anything short of that is correlation following a ramp.

## 3. Why this ranking, and what I expect to be wrong

I ranked by which stage holds the binding constraint, weighing how big the leak is against how
directly product can move it. H1 leads because Stage 3 is the biggest and the last leak, and a
driver's earnings-per-hour logic predicts it with no data at all. H2 follows because Stage 0 sets
the ceiling, even though we have weaker levers on it. H3, the lever under test, lands in the middle
honestly: real, but funded only by a small rider bump under zero-commission, and active at a narrow
margin rather than across the board. H4 sits next to it because it carries the same price story's
other sign and the invisible missing-quote loss. H5 ranks last on base rate but stays in the frame
for its variance.

The belief I most expect to be wrong is H3 read as a broad win, which is exactly the belief
leadership is leaning on. I expect the gains to be narrow: peak, short, busy-area trips, and mostly
in Auto Priority, whose riders care least about an extra ₹15. I expect the rupee effect to be small,
and I expect some of it to leak straight back out at Stage 1 as riders the higher fare pushed to a
cheaper competitor. The multi-homing wrinkle makes me more sure, not less. If the biggest leak is
cancellation, and a real chunk of cancellation is drivers getting poached by a subsidized
competitor, then pricing cannot fix that part at all, because NY cannot outbid a subsidy. My working
bet is that the two-week tick up is mostly H5 and H2, a recovery and a shift in the demand mix,
credited to H3 because the timing happened to line up.

---

### Second-order effects and risks to the test (MECE appendix)

The five hypotheses are stage-exclusive and the stages are exhaustive, so the first-order space is
covered. (Multi-homing was promoted out of this appendix and into H1, since it shapes the Stage 3
leak directly.) These higher-order effects cut across stages and matter for the ship decision:

- **Supply spillover.** Peak surge thickens supply, which lifts completion on un-surged nearby and
  shoulder-hour trips. Threatens the placebo test, so design the placebo far from any surge.
- **Demand learning.** Riders learn the surge timing and start shifting or skipping peak searches,
  eroding the demand base slowly and invisibly inside a five-week window.
- **Composition shift.** Surge changes the mix of trips that finish, moving averages for mix reasons
  rather than behaviour. Read completion within a fixed distance band only.
- **Attribution gaming.** Accept-then-stall flips `cancelled_by_driver` into `cancelled_by_user`, so
  Stage 3 can look better on the driver side while nothing real has changed. Carries into Part 3.
