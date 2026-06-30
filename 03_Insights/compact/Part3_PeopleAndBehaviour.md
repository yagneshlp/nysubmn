# Part 3 — Get Inside Their Heads

*Judgment about people, not analytics.*

## 3.1 — The driver who accepts a ₹67 trip, then cancels

He is not optimising the trip; he is optimising the hour. A ₹67 fare with a 1.5 km pickup means driving six kilometres to get paid for four and a half, dropping his effective rate from ₹15/km to around ₹11 before fuel. He accepted on the only number the offer card showed him, because hesitating risked losing the ping. The cancellation is the first moment the product let him see the real trip. That is a UX failure wearing the costume of a behaviour problem.

He is also missing three things that would settle the decision: the destination (does this drop me somewhere dead?), whether a better ping is seconds away (NY dispatches one at a time; the only rival offer visible mid-hold comes from Uber or Ola, who cannot tell he is busy), and what this corner looks like in twenty minutes. He is making an earnings-per-hour call with almost none of the inputs that decision needs.

Would a congestion bump change his mind? Barely. On the mass tier the surge moved six rupees on a ₹150 fare. Six rupees does not redeem a bad trip, and where it did rise on Auto, completion fell, because the charge fires hardest exactly when the market is most stretched. The money is aimed at the wrong moment; its label and timing are wrong, not just its size.

## 3.2 — Experiment: the legible deadhead

**Hypothesis.** Most driver cancellations on short trips with long pickups are an information problem, not a pay problem. The driver accepts blind to the deadhead, then cancels the instant the product shows it to him.

**Intervention.** Two linked changes on peak slices where a congestion charge already applies (because that is where the rupee to rebrand actually exists):
- The offer card leads with pickup distance and a net-of-deadhead number: "₹67, minus ~₹18 deadhead, ~₹49 net," instead of the bare fare.
- The congestion uplift is renamed and surfaced as "deadhead pay: +₹X for your 1.5 km pickup," converting an abstract area tax into named compensation for the exact friction he cancels over.

The rider sees the same total fare, presented as "busy-area pickup support." Same rupee, one coherent story to both sides.

**Prerequisite.** Audit the live driver app first. The entire experiment rests on one premise: the offer card today shows fare but not deadhead-adjusted economics. If proximity matching or pre-accept transparency is already shipped, this design is moot or must be re-scoped.

**Primary metric.** Driver-cancellation rate on the treated slice vs the same slice the prior week. Cleaner where the funnel allows: honour rate (completed / accepted bookings).

**Guardrail metrics:**
- Acceptance rate and no-quote share (a cancellation pushed upstream is not fixed).
- Completion-per-search and competitor fare gap on the rider side (the fare did not rise; if these move, something leaked).
- Auto and Auto Priority read separately, never blended.

**Gaming surfaces.** Accept-then-stall (driver accepts, sits still, forces rider to cancel): watch `cancelled_by_user` share, time-to-cancellation distribution, and frozen-driver-location patterns after accept. Deadhead farming (hovering past a distance threshold to trigger the bonus): watch pickup-distance distribution for unnatural clustering at the fee boundary.

**The seam I will not hide.** The congestion charge is area-based; the deadhead is trip-based. They only fund each other where they coincide: at peak in busy zones. Off-peak trips with long pickups have no rupee to rebrand, which is exactly why I scope the first test to peak. If it works there, the open question is whether off-peak deadhead is worth funding with an explicit rider pickup fee, which reopens the Stage 1 defection risk and would need its own test.

## 3.3 — The rider who searches and gets nothing

Her moment is short and quiet, which is why it is dangerous. She searches, waits, and either gets no quote or one that is too expensive. She closes the app. Namma Yatri can see the search did not become a ride, but not why: a no-quote, a price-sensitive rejection, and idle curiosity all collapse into the same shortfall, and the app she opened next is invisible.

A no-quote is worse than a cancellation. A cancellation leaves a fingerprint; a no-quote removes a customer and a sliver of network liquidity at once and tells you nothing. On a platform where both sides multi-home, that sliver is gone before you can count it: the driver it would have brought online logs into Uber instead, making the next rider's search harder, which drives the next driver away. The quiet exits are how a marketplace unwinds, one at a time, each making the next more likely.

## 3.4 — From my own life

I moved to a new city for work this year, and the job keeps me on the road about a fifth of the time, so the last twelve months have made me a heavy and slightly obsessive user: north of 200 rides across autos, cabs, and bikes, mostly in Mumbai, Bangalore, and Chennai, with a handful in tier-1.5 cities like Coimbatore and Visakhapatnam. Ride that much in that many places and you stop seeing one market; you start seeing several. A few of the patterns line up uncomfortably well with what the cube said, and one cuts against an assumption baked into this whole brief.

That assumption is that pricing is a single lever that behaves the same way everywhere, and it is not. Multi-homing is universal; every driver I have spoken to runs several apps at once. But what a driver does with a ride he has accepted changes from city to city. In some places asking for a little over the meter is a candid part of the trip, so he accepts and then negotiates; in others the app's own matching does the price discovery, and a driver who finds the fare not worth it simply never quotes, instead of accepting and squeezing. That is not a small UX detail. It means the job a user (rider/driver) hires the app to do is genuinely different in different cities: in one it is a discovery platform that is suggesting price, in another its a full marketplace where price is fixed when match happens. 

The second pattern is about the trips a fare cannot rescue. Weather and the traffic on the specific route impact acceptance far more than the headline number does; I have watched drivers wave off a well-paid trip because the route itself was misery, and some routes are not worth taking even at fifty percent more. That is Part 2's saturation curve seen from the front seat: past a point the driver is pricing the road, not the meter, and another rupee buys nothing. It is also why a one-way run into a deadzone in off-peak hours is a last resort, taken to stop the bleed of sitting idle rather than because it pays; he is managing loss aversion on his earnings per hour, not chasing the trip. 

Fill rates are visibly better on the zero-commission apps, and what decides which app a driver actually favours is rarely the fare; it is the non functional requirements like, how fast the online payment settles and whether a promised promotion really lands. Another qualm is that the pricing is slow to react to cost, taking more than a couple of weeks after fuel price moves to climb back to a driver's real breakeven and the margin he had before. 
