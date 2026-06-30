# Part 3 — Get Inside Their Heads

> **Status: PARKED.** 3.1–3.3 drafted + data-grounded (D-013, D-014). **3.4 pending: user will supply
> personal anecdotes to incorporate here.** Coming back after Part 4.
>
> *Judgment about people, no analytics. Reasoned by the same person who built the funnel spine in
> Part 1 and watched the surge barely move the mass tier in Part 2, now thinking about the humans on
> both sides of that funnel.*

## 3.1 — The driver who accepts a ₹67 trip, then cancels

Picture the trip honestly before you judge him. A ₹67 auto fare on Bangalore's meter is about a 4.5 km
ride, ₹30 for the first two kilometres and ₹15 for each one after. Now add the part the fare never pays
for: a 1.5 km drive to even reach the rider. He is about to drive six kilometres to get paid for four
and a half, which quietly drops his rate from the meter's ₹15 a kilometre to something closer to ₹11
before a drop of fuel is counted. He is not optimising this trip; no driver does. He is optimising the
hour, and the only number that matters to him is what he clears between now and the time he goes home.
A ₹67 fare with a ten-minute unpaid crawl to the pickup is not a ₹67 decision; it is a "what else could
this slot earn me" decision, and the honest answer is often "more."

So he accepts and then cancels, and the accept-then-cancel is not fickleness; it is the app teaching him
to behave that way. He accepts on the only number the offer card shows him, the fare, because hesitating
risks losing the ping. Then the map loads, he sees the 1.5 km pickup sitting between him and the money,
and he does the arithmetic he was never shown up front. The cancellation is the first moment the product
let him see the real trip. That is a UX failure wearing the costume of a behaviour problem.

What he cannot see is most of what would actually settle the decision. He cannot see the destination, so
he cannot tell whether this drops him somewhere dead or somewhere thick with the next fare. He cannot see
whether a better ping is seconds away, because Namma Yatri dispatches him one ride at a time and will not
show him a second while he holds this one; the only rival offer he can ever see mid-hold comes from Uber
or Ola, who cannot tell he is busy. And he cannot see the area's near future, whether this corner empties
out in twenty minutes or fills up. He is making an earnings-per-hour decision with almost none of the
inputs an earnings-per-hour decision needs.

Would a congestion bump change his mind? Barely, and Part 2 is why. On the mass Auto tier the surge moved
the applied multiplier from about 1.06 to 1.07, six rupees on this fare, and six rupees does not redeem a
genuinely bad trip. Worse, where the surge did rise on Auto, completion fell, not rose, because the charge
fires hardest exactly when the market is most stretched. The bump is real money pointed at the wrong
moment: it arrives as a slightly larger fare, not as compensation for the specific thing he is cancelling
over. He is not refusing because the fare is ₹67 instead of ₹73; he is refusing because ₹6 of that is
invisible to him and none of it is named for the 1.5 km he resents. The rupee is almost right. Its label
and its timing are wrong.

## 3.2 — One experiment to cut driver cancellations: the legible deadhead

The experiment follows straight from 3.1: stop adding money and start making the money he already
generates legible, at the moment he decides.

**Step 0, and it is not optional: audit the live driver app first.** I cannot see Namma Yatri's current
offer card, so I will not assume what it shows. The entire experiment rests on one premise, that the card
today surfaces the fare but not the deadhead-adjusted economics, and does not already route a pickup
compensation. If the audit finds proximity matching, a reliability score, or pre-accept transparency
already shipped, this design is either moot or must be re-scoped against what exists. Honesty about the
unknown current state is the first deliverable, not a footnote.

**Hypothesis.** A large share of driver cancellations on short and mid trips with long pickups are
manufactured by an information gap, not a pay gap. The driver accepts blind to the deadhead, then cancels
the instant the product finally shows it to him. If we surface the deadhead-adjusted earning before he
accepts, and route the congestion rupee the rider already pays to him as an explicitly named "deadhead
pay" for that pickup, his accept becomes an informed one and his honour rate rises, with no increase to
the rider's fare.

**Intervention.** Confine it to the peak slices where a congestion charge already applies, because that is
where the rupee to rebrand actually exists, and it is also the only slice Part 2 found a real win. Two
linked changes, shipped together because neither works alone. First, the driver's offer card leads with
pickup distance and a net-of-deadhead number, "₹67, minus ~₹18 to reach the pickup, ~₹49 net," instead of
a bare fare. Second, the congestion-funded uplift on that trip is relabeled and shown to him as "deadhead
pay: +₹X for your 1.5 km pickup," so the surge stops being an abstract busy-area tax and becomes
compensation named for the exact friction he cancels over. The rider sees the same total fare she sees
today, presented as one honest shared story, "busy-area pickup support," so a driver actually comes. Same
rupee, one narrative to both sides; that is the parity. If the rider were told "congestion" while the
driver were told "deadhead," it would be spin, not parity, and the first time the two compared notes it
would break.

**Primary metric.** Driver-cancellation rate on the treated slice, `cancelled_by_driver / rides`, read
against the same slice the week before rather than a broad before-and-after, exactly as Part 2 demanded.
The cleaner cut, where the funnel allows, is the honour rate: completed over accepted bookings.

**Guardrail metrics.** Three, because a cancellation you "fix" by pushing it upstream is not fixed. One,
acceptance rate and the no-quote share: if informed drivers simply decline up front, the loss has only
moved from a late cancel to an early refusal, and a refused trip still strands the rider; an upfront
decline is cheaper than a late cancel, but only if it does not collapse match rate. Two, the rider side,
completion-per-search and the competitor fare gap, which should hold because the fare did not rise; if
they move, something leaked. Three, Auto and Auto Priority watched apart, never blended.

**How I would detect gaming.** Two surfaces. The one the brief names: accept-then-stall, where a driver
accepts to hold the slot, then sits still to force the rider to cancel and flip the blame from his column
to hers. I watch the `cancelled_by_user` share, the distribution of time from accept to cancellation
(stalls cluster at the long tail), and rider cancels that follow a frozen driver location. The second
surface is new and is created by the fee itself: a deadhead pay scaled to pickup distance invites
deadhead farming, drivers drifting to where long-pickup pings pay the bonus, or hovering just past a
distance threshold. I watch the pickup-distance distribution for unnatural clustering at the fee
boundary, and net earnings per online hour to confirm the bonus is buying completed rides rather than
gamed pickups.

**The seam I will not hide.** The congestion charge is area-based and the deadhead is trip-based, so the
two only fund each other where they coincide, in busy zones. An off-peak trip with a long pickup has no
congestion rupee to rebrand, and there this lever has nothing to spend. That is precisely why I scope the
first test to peak and refuse to claim it as a general fix. If it works there, the open question for later
is whether the off-peak deadhead is worth funding with a small explicit rider pickup fee, which reopens
the Stage-1 defection risk Part 2 flagged and would need its own test.

## 3.3 — The rider who searches and gets nothing

Her moment is short and quiet, which is exactly why it is dangerous. She opens the app, types the
destination, and waits through the spinner for a number. Either none comes, because nobody nearby will
quote a trip the meter underprices, or one comes that is high enough or slow enough that she closes the
app. Her search is the one part of this the system does tally; everything that matters about it, it does not.
The data dictionary is explicit on the point: there is no record of the rider who got no usable quote and
left for another app, no ids to follow her, and no fare attached to a quote that never converted, because
the fare columns are measured on completed rides only. So Namma Yatri can see that a search did not become
a ride, but not why: a no-quote, a quote she found too dear, and idle curiosity all collapse into the same
shortfall, and the app she opened next is invisible. It cannot even count the no-match population cleanly,
since retries inflate the acceptance column past the search column and the raw funnel does not subtract to
a tidy "lost rider" number. The single most important failure in the whole funnel is the one the data is
built not to show, and that is not an oversight to fix in this table; it is the structural reason Part 5
will argue the ship decision needs a signal this dataset can never contain.

The damage is that it compounds, and it compounds on the side of the market that is hardest to rebuild.
Every rider who leaves unserved thins demand, and thin demand is what pulls drivers off the platform,
because a driver judges where to log in by where the rides are. Fewer drivers means longer pickups and
more no-quotes, which sends the next rider away faster, which thins demand again. A marketplace does not
fail all at once; it unwinds one silent exit at a time, each one making the next more likely. This is why
a no-quote is worse than a cancellation: a cancellation at least leaves a fingerprint and a rider who
tried, while a no-quote removes a customer and a sliver of liquidity together and tells you nothing. The
congestion charge was built to answer part of this, the underpriced trip nobody quotes, and on the
premium tier at peak it genuinely does. But the rider who already left is not coming back because the next
trip is priced better; liquidity lost is slow to earn back, and the quiet exits are the ones that decide
whether the flywheel spins forward or runs down.

Name this in the language it belongs to. A no-quote is not one lost fare; it is a withdrawal from the
cross-side loop that is the only asset a marketplace truly compounds. More riders make it worth more to
drivers and more drivers make it worth more to riders, and that loop is the slowest thing to rebuild,
because each side waits on the other and you cannot credibly promise a rider cars that are not there. So
the lost rider does double damage: she weakens the pull that would have brought the next driver online,
his logging off weakens the pull that would have held the next rider, and the congestion that drove her
away sits fully intact behind her.

What makes this sharper for Namma Yatri than for a textbook marketplace is that both sides multi-home, so
NY captures less of its own network effect than its size suggests. The driver it brings online with a fair
fare serves Uber the next minute; the value leaks straight across the wall single-dispatch cannot police.
Leaky network effects are why NY cannot simply out-network a subsidised rival into submission, and why the
moat has to be structural, built on cost and tech and trust rather than the raw liquidity lock-in a captive
platform would enjoy. The no-quote hurts most here for exactly that reason: when your own riders and
drivers are one tap from the competition, every silent exit is network capital you may never win back.

## 3.4 — From my own life

I moved to a new city for work this year, and the job keeps me on the road about a fifth of the time, so
the last twelve months have made me a heavy and slightly obsessive user: north of 200 rides across autos,
cabs, and bikes, mostly in Mumbai, Bangalore, and Chennai, with a handful in tier-1.5 cities like Coimbatore
and Visakhapatnam. Ride that much in that many places and you stop seeing one market; you start seeing
several. A few of the patterns line up uncomfortably well with what the cube said, and one cuts against an
assumption baked into this whole brief.

That assumption is that pricing is a single lever that behaves the same way everywhere, and it is not.
Multi-homing is universal; every driver I have spoken to runs several apps at once. But what a driver does
with a ride he has accepted changes from city to city. In some places asking for a little over the meter is
just the local grammar of the trip, so he accepts and then negotiates; in others the app's own matching does
the price discovery, and a driver who finds the fare not worth it simply never quotes, instead of accepting
and squeezing. That is not a small UX detail. It means the job a rider hires the app to do is genuinely
different in different cities: in one it is a discovery platform that should suggest a fair price, in another
a full marketplace that should clear one. A congestion charge tuned to Bangalore is not a global setting,
which is exactly why Part 5 resists shipping the Bangalore result to Delhi or Kolkata on this evidence. What
we would be scaling is more local than the dashboard makes it look.

The second pattern is about the trips a fare cannot rescue. Weather and the traffic on the specific route
drive acceptance far more than the headline number does; I have watched drivers wave off a well-paid trip
because the route itself was misery, and some routes are not worth taking even at fifty percent more. That is
Part 2's saturation curve seen from the front seat: past a point the driver is pricing the road, not the
meter, and another rupee buys nothing. It is also why a one-way run into a deadzone in off-peak hours is a
last resort, taken to stop the bleed of sitting idle rather than because it pays; he is managing loss aversion
on his earnings per hour, not chasing the trip. The deadhead to a pickup is fine when the ride makes up for
it; what actually stings is the last-minute rider cancellation after he has already driven over, which is the
same wound Part 3 wants to stop blaming only on drivers.

The last pattern is why I believe the premium-tier finding is real. Among my own people, peers and family
both immediate and extended, Namma Yatri has a specific reputation: the bit extra you pay comes back as
well-behaved, prompt, professional drivers and a near-certain match inside a minute. That is Finding 1 from
the rider's seat; the Auto Priority rider is buying reliability, and it is the one slice where the charge
genuinely earned its keep. The structural half shows up too. Fill rates are visibly better on the
zero-commission apps, and what decides which app a driver actually favours is rarely the fare; it is the
boring plumbing, how fast the online payment settles and whether a promised promotion really lands. And the
stale meter is not only blind to the hour; it is slow on cost, taking more than a couple of weeks after a fuel
move to climb back to a driver's real breakeven and the margin he had before. The gap that opens in those
weeks is the exact place his "is this worth it" math turns against the trip, and the exact place the
congestion work is trying to reach.
