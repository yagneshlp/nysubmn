# Part 1 — Frame the Problem

*First-principles reasoning. No ride data opened.*

Completed rides are the last survivor of four multiplied stages. Nothing moves the number without moving one of those terms, which means the congestion charge is not a general lever; it is a two-signed force living in two specific spots: pulling a driver in at Stage 2, and potentially pushing a price-sensitive rider out at Stage 1.

<figure class="funnel">
  <div class="funnel-out">completed rides <span class="funnel-eq">=</span></div>
  <div class="funnel-chain">
    <div class="stagebox"><span class="stage-k">Stage 0</span><span class="stage-f">searches</span><span class="stage-d">demand volume</span></div>
    <span class="op">&times;</span>
    <div class="stagebox price"><span class="stage-k">Stage 1 <span class="price-tag">price &minus;</span></span><span class="stage-f">accepted/search</span><span class="stage-d">rider gets a usable quote &amp; accepts</span></div>
    <span class="op">&times;</span>
    <div class="stagebox hit"><span class="stage-k">Stage 2 <span class="hit-tag">price +</span></span><span class="stage-f">ride/accepts</span><span class="stage-d">a driver accepts &amp; matches</span></div>
    <span class="op">&times;</span>
    <div class="stagebox"><span class="stage-k">Stage 3</span><span class="stage-f">1 &minus; cancel</span><span class="stage-d">booking is honoured</span></div>
  </div>
  <figcaption>The one link the congestion charge is built to move is to pull a driver into Stage 2. The same charge pushes the other way at Stage 1, where a higher fare can send a price-sensitive rider to a cheaper competitor. One lever, two signs, two stages.</figcaption>
</figure>

## Ranked hypotheses

**H1 — Stage 3: driver cancellation. [Most likely]**
The driver optimises his hour, not this trip. A ₹67 fare with a 1.5 km pickup earns him around ₹11/km effective after deadhead, not the meter's ₹15. He accepted on the only number the offer card showed him; the cancellation is the first moment the product let him see the real trip. Multi-homing sharpens it: the only rival offer visible while he holds your booking comes from Uber or Ola, and NY cannot outbid a subsidized competitor on a per-trip basis.

**H2 — Stage 0: demand volume. [High]**
Sets the ceiling above everything downstream. Moves with competitor subsidies, the calendar, and paydays; mostly outside our control. Product has fewer real levers here than on cancellation.

**H3 — Stage 2: getting the driver to accept the ride. [Medium; the lever under test]**
The congestion bump lifts the fare on the trips the old meter underprices at peak. Works at the exact margin of a skipped trip; disappears in the average. A ₹8 nudge on a ₹75 fare.

**H4 — Stage 1: the rider's side. [Medium; the invisible one]**
Two failures: the rider who gets no ride at all (a supply-thinness problem, invisible in the data), and the rider who gets priced off our platform. Same dial, opposite sign.

**H5 — External forces: weather, calendar, competitor spend. [Low base rate, high variance]**
The most likely candidate to be doing the work the pricing gets credit for, given the timing coincidence.

## How I'd tell cause from coincidence

The rollout was never a clean A/B: version assignment was observational and outcome-dependent, with winning versions ramped toward 100% fast. A slice must clear five tests in order before I credit the pricing:

1. **Price moved.** Rebuild applied multiplier from `congestion_sum / congestion_n`. If it never rose, stop here.
2. **Like-for-like.** Same tier, distance band, and hour against the identical slice a week prior, so confounds are held still rather than averaged away.
3. **Clean comparison window.** v250 vs v252 inside the same peak hours: time of day matched, pricing logic the only variable left.
4. **Dose-response + placebo.** Completion rises more where surge rose more, and stays flat where price never moved.
5. **Denominator check + both sides.** Track raw completed rides, not just the ratio. Compare NY fare to competitors at Stage 1 (defection risk) and Stage 3 (poach risk) simultaneously.

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
and I expect some of it to leak straight back out at Stage 1 as riders with the higher fare are pushed to a
cheaper competitor. The multi-homing angle makes me more sure, not less. If the biggest leak is
cancellation, and a real chunk of cancellation is drivers getting poached by a subsidized
competitor, then pricing cannot fix that part at all, because NY cannot outbid a subsidy. My working
bet is that the two-week tick up is mostly H5 and H2, a recovery and a shift in the demand mix,
credited to H3 because the timing happened to line up.
