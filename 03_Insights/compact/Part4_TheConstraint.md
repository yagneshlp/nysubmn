# Part 4 — The Constraint

*Win-win growth under zero-commission, a stale meter, and no subsidy.*

## Why raising the fare is the wrong lever

Under zero-commission, every rupee of the congestion charge comes from the rider at one-to-one. It saturates near 1.5x. And it aims at the wrong leak: the driver cancelling over an unpaid deadhead and the rider getting no usable quote are not problems a price change fixes. NY has nominal headroom, about 17% below the cheaper rival on mass Auto at peak, but spending that cushion is the wrong move because the cushion is the moat. NY's durable advantage over a subsidized rival is being the cheapest honest option built on the lowest cost to serve; you do not defend that by becoming less cheap. The right move is to stop buying completion with money NY does not have and start buying it with the asset it does own: data and prediction.

## The option space

A completed ride needs exactly three things to coincide: a rider who asks, a driver who is willing and near, and a match that holds. Nothing else matters. Every conceivable lever moves exactly one of these, which makes **demand, supply, and match** a complete, non-overlapping segments of the whole solution space.

<figure class="journey">
  <div class="journey-head">A completed ride needs three things to coincide: a rider who asks, a driver who is willing and near, and a match that holds. Every lever moves exactly one of them, so <strong>demand, supply, and match</strong> partition the whole space. Walk each along its journey, and the map funnels to one lever.</div>

  <div class="lane">
    <div class="lane-side"><span class="lane-name">Demand</span><span class="lane-verdict">This is Rider facing </span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">all riders · consideration</span><span class="chip-l">Public-good trust · ONDC discovery</span></div>
      <div class="chip"><span class="chip-p">Commuter · intent</span><span class="chip-l">Intent-ahead booking</span><span class="chip-note">declare the 6pm trip at noon, it becomes the supply forecast</span></div>
      <div class="chip"><span class="chip-p">Spontaneous · quote</span><span class="chip-l">No-quote fallback</span><span class="chip-note">capture the silent exit as a signal, not a loss</span></div>
      <div class="chip"><span class="chip-p">price-sensitive · flex</span><span class="chip-l">Name-your-time</span><span class="chip-note">a small reward to shift off-peak, flattening the peak that leaks</span></div>
    </div>
  </div>

  <div class="lane hit">
    <div class="lane-side"><span class="lane-name">Supply</span><span class="lane-verdict">This is Driver facing.</span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">Full-timer · go-online</span><span class="chip-l">Predictive go-online nudge</span></div>
      <div class="chip star"><span class="chip-p">Full-timer · positioning</span><span class="chip-l">Supply-shaping &#9733;</span><span class="chip-note">reposition cars ahead of forming demand, using data NY already owns</span></div>
      <div class="chip"><span class="chip-p">Full-timer · offer</span><span class="chip-l">Legible deadhead</span><span class="chip-note">the Part 3 experiment</span></div>
      <div class="chip"><span class="chip-p">Full-timer · post-drop</span><span class="chip-l">Back-haul intelligence</span></div>
    </div>
  </div>

  <div class="lane">
    <div class="lane-side"><span class="lane-name">Match</span><span class="lane-verdict">This is how a rider and driver are connected.</span></div>
    <div class="lane-chips">
      <div class="chip"><span class="chip-p">platform · dispatch</span><span class="chip-l">Proximity-first dispatch</span></div>
      <div class="chip"><span class="chip-p">Commuter &harr; Full-timer · hold</span><span class="chip-l">Committed / standing rides · pooling</span></div>
      <div class="chip"><span class="chip-p">both sides · loyalty</span><span class="chip-l">Reliability membership</span></div>
    </div>
  </div>

  <figcaption><strong>The map funnels to supply-shaping.</strong> Demand levers feed the forecast; match levers are the endgame density unlocks later. Position the cars now with data that costs nothing, then graduate the reliable pairs into committed rides once the liquidity is real.</figcaption>
</figure>

**Where the map converges.** At evening peak, the moment the funnel leaks most, demand is not the scarce input; most searches are happening right then. The binding constraint is supply not being where they ask. Demand-side levers feed the forecast but do not close the gap. Match-structure fixes like committed rides are the most complete answer, but they rest on a promise of dense, reliable supply that does not yet exist. That leaves the supply column, and within it positioning, as the one cell where the binding constraint, the data we actually have, and the zero-rupee limit all intersect.

## Competitor read and the defection risk of pricing higher

Comparing within distance band matters here; the competitor scrape skews long (~16 km median) and a pooled average is distance-confounded.

- **Mass Auto at peak:** NY sits ~17% below the cheaper rival, deepest on short trips (28% under at 1-2 km). Real headroom, but spending it is the wrong call; the cushion is the moat.
- **Auto Priority peak at 3-6 km:** NY already sits above the cheaper rival by 3-12%. That is the same slice Part 2 credited as the one real pricing win. Raise congestion there and you cross the market in the exact bands that were carrying the result, with a subsidized rival one tap away.

## The defended lever: supply-shaping

**The idea.** Position drivers ahead of predictable demand. A driver idling in a thinning zone gets a concrete, self-interested nudge toward a forming hotspot in his own terms: "Move 1.2 km to Indiranagar; 18 searches forming there in 15 minutes, average pickup 0.4 km against your 1.5 km here." Not a price change, not a subsidy; the platform spending its information to put the right car near the right rider before either has to settle for a bad match.

**The honest prerequisite.** This lever does not run on the current cube since geography is the missing input. a repositioning nudge is geography dependant. The first step is the instrumentation: log pickup distance, tag supply and demand to zones. That signal exists in the operational system today, because NY already runs this dispatch; it simply never reached the analysis cube. The gap is instrumentation and access, not a missing capability.

**Why demand is forecastable enough.** Weekday search volume by hour is highly regular (median hourly CV ~0.26). The evening peak's timing and location recur every weekday. Completion-per-search hits its worst of the day at 6-7 pm (0.37 and 0.35), with cancellations at their daily high. The biggest, most forecastable hole in the funnel announces itself on a schedule.

**Win-win-win.** The driver wins first: shorter pickups mean less unpaid deadhead, which lifts his rupees-per-hour, the exact number Part 3 said the bad trip was wrecking. The rider wins because a pre-positioned car converts her search into a quote. NY wins because thicker liquidity at the predictable peak is completion without subsidy, and every pickup it shortens is network capital it keeps rather than leaks.

**Zero marginal cost at scale.** The prediction runs on data NY already holds and compute it already owns. A subsidized rival grows completion by spending money it does not make; NY grows it by spending intelligence it already has.

**The second-order risk.** A naive broadcast that tells every idle driver about the same hotspot creates a glut where they land and a new shortage where they left. The fix is allocation, not announcement: send roughly as many cars as the forming demand can absorb, stagger the nudges, and read supply alongside demand. A nudge that proves wrong a few times gets ignored forever; the prediction has to be good before it ships.

**Why this one first.** Supply-shaping thickens the base that makes everything downstream credible. Committed rides are the more complete fix, but they require guaranteed supply density that does not yet exist. Build the density with information that costs nothing, then graduate reliable pairs into standing rides once the liquidity is real. NY does not have the subsidy to buy its way to that density; it has the data to route there.
