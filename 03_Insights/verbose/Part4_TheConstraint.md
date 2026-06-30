# Part 4 — The Constraint

> *How to grow completed rides win-win under zero-commission, a stale meter, and no subsidy, where
> every rupee must pay for itself. The menu, the competitor read, and one lever defended.*

## Is raising the fare even the right lever?

No. It is a patch, and Parts 2 and 3 already showed the seams. The congestion charge is the only dial
zero-commission leaves on driver pay, so every rupee of it comes from the rider at one-to-one, it
saturates near 1.5x, and it aims at the wrong leak: the two things actually losing completed rides are
the driver cancelling over an unpaid deadhead and the rider getting no usable quote and leaving, and
neither is a price the meter can fix. There is even nominal room to raise it; within distance band at
peak NY still sits about 17% under the cheaper rival on the mass tier. But spending that cushion is the
wrong move, because the cushion *is* the moat. NY's durable advantage over a subsidized rival is being
the cheapest honest option built on the lowest cost to serve; you do not defend that by becoming less
cheap. The right move under the constraint is to stop buying completion with rupees, which NY does not
have to spare, and start buying it with the asset NY does own outright: data and prediction.

## The option space, decomposed

The brief asks for invention, not a riff on its examples, so I start from a spine that is MECE by
construction rather than a brainstorm. A completed ride needs three things to coincide in the same place
at the same moment: a rider who asks, a driver who is willing and near, and a match that holds. Nothing
else exists. Every conceivable lever moves exactly one of these three, which makes **demand, supply, and
match** a complete and non-overlapping partition of the whole solution space. I walk each one along its
customer journey, naming the persona, the job they are hiring the app to do, and the pain that breaks the
ride, then I locate the binding constraint and let the data choose the lever.

The personas matter because they are not interchangeable. On the rider side there is the **Commuter** (a
fixed A-to-B at a fixed hour, hiring the app for certainty at peak), the **Spontaneous rider** (price-first,
hiring it for a cheap car now), and the **Premium rider** (Auto Priority, hiring it for reliability over
price). On the driver side there is the **Full-timer** (an earnings-per-hour maximizer who multi-homes and
hates unpaid time), the **Opportunist** (logs in only for the peak), and the **Loyalist** (NY-first on
trust). The ride that leaks most in our data, the evening-peak short trip, is the Commuter meeting the
Full-timer, and that pairing is where the whole analysis converges.

<figure class="journey">
  <div class="journey-head">A completed ride needs three things to coincide: a rider who asks, a driver who is willing and near, and a match that holds. Every lever moves exactly one of them, so <strong>demand, supply, and match</strong> partition the whole space. Walk each along its journey, and the map funnels to one lever.</div>

  <div class="lane">
    <div class="lane-side"><span class="lane-name">Demand</span><span class="lane-verdict">Not the scarce input at peak (most searches are there). Ruled out as the binding constraint; these feed the forecast.</span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">all riders · consideration</span><span class="chip-l">Public-good trust · ONDC discovery</span></div>
      <div class="chip"><span class="chip-p">Commuter · intent</span><span class="chip-l">Intent-ahead booking</span><span class="chip-note">declare the 6pm trip at noon, it becomes the supply forecast</span></div>
      <div class="chip"><span class="chip-p">Spontaneous · quote</span><span class="chip-l">No-quote fallback</span><span class="chip-note">capture the silent exit as a signal, not a loss</span></div>
      <div class="chip"><span class="chip-p">price-sensitive · flex</span><span class="chip-l">Name-your-time</span><span class="chip-note">a small reward to shift off-peak, flattening the peak that leaks</span></div>
    </div>
  </div>

  <div class="lane hit">
    <div class="lane-side"><span class="lane-name">Supply</span><span class="lane-verdict">The binding constraint, and where the data and the zero-rupee limit intersect. This is where the map converges.</span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">Full-timer · go-online</span><span class="chip-l">Predictive go-online nudge</span></div>
      <div class="chip star"><span class="chip-p">Full-timer · positioning</span><span class="chip-l">Supply-shaping &#9733;</span><span class="chip-note">reposition cars ahead of forming demand, using data NY already owns</span></div>
      <div class="chip"><span class="chip-p">Full-timer · offer</span><span class="chip-l">Legible deadhead</span><span class="chip-note">the Part 3 experiment</span></div>
      <div class="chip"><span class="chip-p">Full-timer · post-drop</span><span class="chip-l">Back-haul intelligence</span></div>
    </div>
  </div>

  <div class="lane">
    <div class="lane-side"><span class="lane-name">Match</span><span class="lane-verdict">The most complete fixes, but they rest on supply density that does not exist yet. The staged endgame, not the first move.</span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">platform · dispatch</span><span class="chip-l">Proximity-first dispatch</span></div>
      <div class="chip"><span class="chip-p">Commuter &harr; Full-timer · hold</span><span class="chip-l">Committed / standing rides · pooling</span></div>
      <div class="chip"><span class="chip-p">both sides · loyalty</span><span class="chip-l">Reliability membership</span></div>
    </div>
  </div>

  <figcaption><strong>The map funnels to supply-shaping.</strong> Demand levers feed the forecast; match levers are the endgame density unlocks later. Position the cars now with data that costs nothing, then graduate the reliable pairs into committed rides once the liquidity is real.</figcaption>
</figure>

## Reading the map: where the binding constraint actually is

A MECE map is only useful if it tells you which cell to act on, and the data does. Demand is not the
scarce input at the moment we leak: the evening peak is the hour with the *most* searches, so the problem
is not too few riders asking, it is supply not being where they ask. That rules the demand column out as
the binding constraint, however clever intent-ahead and no-quote fallback are as companions. The
match-structure levers, committed rides and pooling, are the most complete fixes on the map, but every
one of them rests on a promise of dense, reliable supply that does not exist yet; they are downstream of
solving supply first. That leaves the supply column, and within it the positioning row, as the one place
where the binding constraint, the data we actually hold, and the zero-rupee constraint all intersect. The
map does not just list options; it funnels to one.

So I keep the rest of the map as a deliberately sequenced roadmap rather than a discarded pile.
Intent-ahead booking and the no-quote fallback are the demand-side companions that *feed* the supply
forecast and convert invisible exits into signal. Committed rides and pooling are the match-structure
endgame that supply density unlocks later. The lever I defend now is the one that earns the right to all
of them: supply-shaping.

## Where NY sits, and the defection risk of pricing higher

The brief asks where NY stands against competitor1 and competitor2 and what breaks if we price congestion
up. The clean read is within distance band, because the competitor scrape skews long (~16 km median) and
a pooled average is distance-confounded; a naive pooled peak comparison makes NY look only ~2% cheaper,
which is an artifact, not the truth. Within band at peak the picture splits by tier and it matters.

On the mass Auto tier NY carries real headroom, about 17% below the cheaper rival on a volume-weighted
basis, deepest on short trips (1-2 km is 28% under). So a higher charge would not immediately price Auto
riders above the market. But on Auto Priority at peak the headroom is mostly gone, and in the 3-6 km bands
NY already sits *above* the cheaper rival, by 3% to 12%. That is the same slice Part 2 credited as the one
real pricing win. So the defection risk is not uniform; it is concentrated exactly where the pricing
appeared to work. Push congestion higher and on Auto you spend the cushion on the wrong leak, while on
Auto Priority peak you cross the market in the precise bands that were carrying the result, and a
subsidized rival is one tap away to catch the rider you just overpriced. Either way the fare is the wrong
thing to raise, which is the whole case for moving supply instead of moving price.

## The defended lever: supply-shaping

**The idea.** NY can know, with usable accuracy, when and where the next hour's demand will land; the
*when* is already visible in the data we were handed, and the *where* sits in NY's live dispatch system
one instrumentation step from reach. Use it to position drivers ahead of demand: a driver idling in a
thinning zone gets a concrete, self-interested nudge toward a forming hotspot, framed in his own currency.
"Move 1.2 km to Indiranagar; eighteen searches forming there in the next fifteen minutes, average pickup
0.4 km against your 1.5 km here." It is not a price change and not a subsidy. It is the platform spending
its information to put the right car near the right rider before either of them has to settle for a bad
match.

**The honest prerequisite, stated before the pitch, not buried under it.** This lever does not run on the
cube we were handed, and I will not pretend it does. Part 5 says plainly that this dataset carries no
geography, and a repositioning nudge is geography or it is nothing. So I am not claiming supply-shaping
ships next sprint on the data NY exposes in this table; I am claiming it is the right thing to *build
toward*, and that the first step is the exact zone-level instrumentation Part 5 already demands for its
own sake: log pickup distance, and tag supply and demand to zones. The signal exists in the operational
system today, because NY runs this dispatch; it simply never reached the analysis cube. The gap is
instrumentation and access, not a missing capability, and that is what makes this a sequenced bet rather
than a fantasy. Instrument the geo, prove the forecast against held-out hours, then ship the nudge. The
sequence is the strategy, and everything below is why the build is worth starting now rather than later.

**Why every rupee pays for itself.** It costs essentially nothing at the margin. The prediction runs on
data NY already holds and compute it already owns; there is no per-trip payout, no fare uplift, no burn.
This is the deepest reason it fits the constraint better than anything that touches price: a subsidized
rival grows completion by spending money it does not make, and NY would grow it by spending intelligence
it already has. That is the cost-and-tech moat used as a weapon instead of described in a deck.

**Why it works, in the data.** Two facts make this more than a slogan. First, demand is predictable enough
to shape against: weekday search volume by hour is highly regular, with a median hourly coefficient of
variation around 0.26 and the midday hours steadier still, and the morning and evening commute peaks recur
every weekday. The exact height of the evening peak wobbles, but its timing and place do not, and timing
and place are what positioning needs. Second, the completion loop leaks hardest at exactly that
predictable peak: completion-per-search falls to about 0.37 at 6 pm and 0.35 at 7 pm, its worst of the day,
with cancellations at their daily high. The biggest, most forecastable hole in the funnel is the one a
repositioned car fills. We are not guessing where to send supply; the leak announces itself on a schedule.

**Why it is win-win-win.** The driver wins first and that is the point, because he is independent and a
nudge only works if it pays him: a shorter pickup is less unpaid deadhead, which lifts the rupees-per-hour
he actually optimizes, the same number Part 3 said the bad trip was wrecking. The rider wins because a car
positioned ahead of her search is the difference between a usable quote and the silent no-quote that sends
her to Uber. NY wins because thicker liquidity at the predictable peak is completion bought without
subsidy, and because every pickup it shortens is network capital it keeps rather than leaks.

**Who loses, and the second-order risk I will not hide.** The honest failure mode is herding. A naive
broadcast that tells *every* idle driver about the same hotspot creates a new shortage where they left and
a glut where they land, and oscillation is worse than inaction. So the design has to allocate, not
announce: send roughly as many cars as the forming demand can absorb, stagger the nudges, and read supply
as well as demand. The second risk is trust. A nudge that proves wrong a few times gets ignored forever,
because the driver is under no obligation to follow it, so the prediction has to be good before it ships
and honest about its confidence when it is not. And it does nothing for the thinnest zones and hours where
there is too little signal to forecast; there, it simply abstains. None of these sink the lever; they
scope it to where it is strong, which is the recurring peak it was built for.

**Why this one, and why first.** It is the lowest-risk, lowest-cost move that touches both real leaks at
once, and it asks nothing of either side that is not already in their interest. That is also why it comes
before committed rides rather than instead of it. Committed rides is the more complete fix, but it rests on
a promise of guaranteed supply, and you cannot make that promise on a thin, defectable base. Supply-shaping
is how you thicken the base: position the cars, win the peaks, raise the count of reliably active drivers,
and earn the density that finally makes a standing-ride guarantee credible. The sequence is the strategy.
Shape supply now with information that costs nothing; once the liquidity is real, graduate the most
reliable pairs into committed rides and close the loop for good. NY does not have the subsidy to buy its
way to that density. It has the data to route its way there.
