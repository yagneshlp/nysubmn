# Part 2 — Did the Pricing Work?

> **Status: PARKED FOR REVIEW.** Drafted with figures + structural section (D-011, D-012). Still
> needs scrutiny pass before final. Coming back after Part 3.
>
> *Two reputation-grade findings on specific slices, and the alternatives I ruled out to get
> there. Built by running Part 1's five-test ladder on the cube, not by reading a before-and-after.*

Leadership's number is real and I can reproduce it to the decimal: all-Auto completion-per-search
went 0.496 to 0.569 across the rollout, a +14.9% lift. The question is not whether that ratio rose;
it plainly did. The question is whether *completed rides grew because of the congestion charge*, and
those are not the same claim. A ratio can climb because the numerator grew or because the denominator
shrank, and a charge that only fires at peak cannot be credited for hours where it never fired. So I
put every slice through the ladder from Part 1: did the price actually move, does completion track
the dose, does it stay flat where there was no dose, and does the raw count of finished rides agree
with the ratio. Two findings survived that gauntlet, and they point in opposite directions.

The single chart that frames both is the dose-response, the same 250-versus-252 peak comparison read
separately for each tier. The two tiers do not just differ in degree; they have opposite signs.

![Dose-response: more surge lifts completion on Auto Priority (r=+0.80) but tracks lower completion on Auto (r=−0.72)](../02_Research/plots/fig1_dose_response.png)

## Finding 1 — On Auto Priority, at peak, the pricing genuinely works. It is small, specific, and real.

This is the one slice where I will stake my reputation on the charge *causing* the lift. The clean
test the rollout left behind is versions 250 and 252 running side by side inside the same peak hours,
same tier, same distance bands, so the only thing varying is the pricing logic. On Auto Priority that
comparison shows a textbook dose-response: the distance bands where 252 added the most surge are
exactly the bands where completion rose the most. At 4-5 km the applied multiplier went 1.41 to 1.52
and completion went 0.770 to 0.890; at 9-10 km a similar surge bump bought a +0.145 jump. The long
bands where 252 barely changed the surge, 12-16 km and beyond, show no lift at all. Across the bands
the correlation between how much surge rose and how much completion rose is +0.80. And it is not
riding on thin cells, which is the first thing to suspect on a premium-tier peak slice: every band in
the comparison carries a real sample, the lightest near 1,100 searches and most between two and five
thousand, so no single noisy cell is steering the line. Weight the correlation by sample size and it
stays +0.80 to the decimal. That is not a mix-shift and it is not a coincidence riding a ramp; it is
the lever doing precisely the job Part 1 predicted it was built for, on the riders who care least
about an extra ₹15.

It clears the competitor gate too, which is what lets me call it a win rather than an artifact. Across
every distance band Namma Yatri is the *cheaper* option, 5% to 33% under the nearest rival within the
same distance band, and on Auto Priority it drifted *cheaper* still over the rollout, from a −10% peak
gap to −18%. So nobody was priced out at the rider's end; the higher fare did not leak straight back
out as defections to Uber or Ola, because there was nowhere cheaper to defect to.

The honest caveat is the ceiling. When I bin Auto Priority peak trips by the surge actually applied
inside a fixed distance band, completion traces an inverted-U: it climbs from the low-surge bin to the
mid-surge bin, around 1.4x, then *falls* in the high-surge bin near 1.6x. The 250-to-252 move lived in
the productive part of that curve. Push the same dial past roughly 1.5x and it stops helping and starts
hurting, which is the difference between a calibrated lever and a blunt one.

![Surge saturation: Auto Priority completion peaks near 1.4x then falls; Auto declines throughout](../02_Research/plots/fig2_saturation.png)

## Finding 2 — The headline +14.9% is mostly not the pricing. Three independent tests say so.

The number leadership is leaning on does not survive contact with the ladder, and it fails in three
separate ways that do not depend on each other.

First, on the mass Auto tier the dose-response runs *backwards*. In the same 250-versus-252 peak
comparison, 252 completes a couple of points better in every band, but it does so with *equal or
slightly lower* surge and a lower average fare, ₹152 against ₹154. Whatever earns 252 its edge on Auto,
it is not the congestion charge, because the charge moved the wrong way. Worse, when I bin Auto peak
trips by the surge actually applied within a fixed band, more surge tracks *less* completion: at 4-5 km,
completion falls from 0.518 in the low-surge bin to 0.372 in the high-surge bin. That sign is not a
paradox once you remember the surge is endogenous; it fires hardest exactly when the market is most
congested and supply is most stretched, which are the same moments completion is hardest. On the mass
tier the congestion charge is a thermometer reading the stress, not a medicine relieving it. The left
panel of the dose-response chart above is that failure in a single line: the slope runs the wrong way.

Second, the placebo lights up. A charge that only acts at peak cannot move hours where it never moved,
yet completion rose just as much in the no-surge hours as in the surged ones. On Auto at night the
applied multiplier sat flat near 1.0 and completion still went 0.335 to 0.437; off-peak it went 0.430
to 0.522, gains as large as anything at peak. Part 1 warned that peak surge can thicken supply and
spill into the shoulder hours, so I sited the placebo at night and off-peak and read it inside fixed
distance bands; even with that correction the lift shows up where there is no dose. Something
system-wide moved completion, the charge is not it, and I can name what is, in two pieces, neither of
them the congestion dial. First, a version swap hides inside the rollout. The no-surge hours ran
mostly on the old acceptance-first logic before, v211 at about 47% of off-peak and night searches, and
on the newer baseline plus v250 after, v236 and v250 together near 88%; at an identical ~1.0 surge
those newer versions simply clear better, 0.596 against 0.558. That gain is real, but it lives in the
matching and acceptance logic, not in the congestion add-on the AI is crediting. Second, and more
damning, at peak where the headline lift is largest the cancellation rate did not move a hair, 0.325
to 0.325, and completed-per-ride sat flat at 0.676; the funnel honoured no extra booking, and
completion-per-search rose only because the search base thinned beneath it. A flat cancellation rate
on a marketplace whose biggest leak is cancellation is not a clean bill of health; it is the charge
doing nothing for the one thing that matters most.

![Placebo: Auto completion rose +10% off-peak and +16% at night, where surge never moved, as much as the +19% at peak](../02_Research/plots/fig3_placebo.png)

Third, and most damning, the raw count of finished rides will not carry the ratio's story. Completion-
per-search can rise simply because searches fell, so I tracked the number leadership actually cares
about, completed rides per day. On Auto it ran 82,900 in the back half of May, recovered to 88,900 in
the first nine days of June, then reached 91,800 after the rollout. I will not overclaim against my own
case: that last leg is real, a genuine +3.2% in finished rides, and I am not going to wave it away. But
it is a sliver of the +14.9% the ratio reports, and the gap between the two is pure denominator. Most of
the recovery happened *before* the charge shipped, and the post-rollout leg came on a *falling* search
base, 181,000 searches a day down to 168,000. The ratio jumped far more than the rides did because fewer
people were asking. Auto Priority is starker still: its completed rides per day
actually *fell* after the rollout, from 16,900 to 15,900, the lowest of the whole window, even as its
completion ratio "rose" from 0.664 to 0.767. That entire improvement is a denominator collapsing from
25,400 searches a day to 20,800. The tier the AI analysis crowned the big winner finished fewer rides,
not more.

![Raw count vs ratio: completion ratio climbs for both tiers while completed rides stay flat on Auto and fall on Auto Priority, as searches drop](../02_Research/plots/fig4_count_vs_ratio.png)

## Alternatives ruled out

I considered the obvious confounds and closed them before staking the two findings. The peak-versus-
off-peak mix-shift, the Simpson's trap the brief warns about, is not driving the headline: search-share
by time-of-day barely moved across the rollout, 63% to 62%, and the lift persists inside each
time bucket, so it is not an artifact of the cohort re-weighting toward peak. Distance composition is
controlled by construction, because every comparison above is read within a fixed distance band rather
than pooled, so the lift is not surge quietly filtering short unprofitable trips out and longer ones in.
Rider price-defection is ruled out by the competitor gate: Namma Yatri stayed materially cheaper than
both rivals throughout, so the higher peak fare did not push price-sensitive riders off the platform.

What is ruled *in* is mundane. The bulk of the two-week tick-up is demand recovery that began before the
charge shipped, a completion ratio inflated by a shrinking search denominator, and a version swap in the
off-peak hours that improved matching without ever touching the congestion dial, with a genuine but
narrow conversion win layered on top in Auto Priority at peak. The timing lined up with the rollout, and
the rollout took the credit.

## The structural reason pricing is a weak lever: flat pass-through versus commission

There is a deeper reason the charge reaches so little, and it sits in the business model, not the data.
Namma Yatri is zero-commission, so the fare the rider pays *is* the money the driver takes home; the two
numbers are the same number. Uber and Ola run a commission model, which decouples them: the rival can
charge the rider ₹100, keep a cut, and still hand the driver ₹90 by topping the trip up from its own
balance sheet. That difference changes how to read the competitor chart below. Across every distance band
Namma Yatri is the cheaper option to the *rider*, but a flat fare is also the driver's whole take, while a
competitor's listed fare is the driver's take *minus commission plus subsidy*. So the scrape tells me what
each rider sees and nothing about what each driver nets, and the driver's number is the one that governs
the poach. I can rule out rider defection on price; I cannot see the driver side of a commission book.

![Competitor guard: NY is the cheapest rider option in every distance band, but a flat fare equals the driver take so the rival driver payout stays unseen](../02_Research/plots/fig5_competitor_gap.png)

This is the structural floor under Part 1's H1. Because every rupee of driver pay must come from the
rider at one-to-one, the congestion charge is the *only* instrument Namma Yatri has to lift driver
earnings, and it hits rider price-sensitivity the instant it moves. A subsidized rival funds a better
driver offer from investor money and a commission pool; Namma Yatri funds its ₹8 from the rider's pocket
in full view. You cannot outbid a subsidy when you take nothing from the fare. That is almost certainly
why the Auto Priority dose-response saturates near 1.5x: under flat pass-through the surge is fully
visible to the rider, so it reaches the Stage-1 ceiling fast. The pricing lever is not just empirically
small; it is structurally capped, and the cap is the zero-commission promise itself.

## What the data cannot tell us here

Two gaps bound these findings and I will not pretend past them. The competitor scrape does not carry
Namma Yatri's own ETA, so I can rule out rider defection on *price* but not on *wait time*; a rider who
left because the pickup was twenty minutes out is invisible. And the cube has no rider who searched, got
no usable quote, and left without a trace; the single most important Stage-1 loss is the one moment the
data structurally cannot see. Both reinforce Finding 2's direction rather than soften it.

## Verdict

The congestion charge works where Part 1 said it should and nowhere it shouldn't: a real, bounded
conversion win on Auto Priority at peak, and essentially nothing on the mass Auto tier, where the
headline lift is recovery and arithmetic wearing the charge's clothes. And it cannot be otherwise,
because under zero-commission the charge is the only dial Namma Yatri has on driver pay and it is capped
by rider price-sensitivity the moment it turns. Do not scale it as a broad completion lever. Keep it as
a narrow premium-tier instrument, calibrated below its ~1.5x ceiling, and go looking for the real leak
elsewhere, which Part 1 already named as cancellation.
