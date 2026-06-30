# Part 2 — Did the Pricing Work?

The +14.9% headline is real; I can reproduce it to the decimal. It is also mostly not the pricing. Two findings survive five causation tests, and they point in opposite directions.

The chart that frames both: the dose-response, the 250-vs-252 peak comparison split by tier. The two tiers do not just differ in degree; they have opposite signs.

![Dose-response: more surge lifts completion on Auto Priority (r=+0.80) but tracks lower completion on Auto (r=−0.72)](../02_Research/plots/fig1_dose_response.png)

## Finding 1 — Auto Priority at peak: the pricing genuinely works. Small, specific, and real.

- v250 vs v252 inside the same peak hours, same tier, same distance bands. Only the pricing logic varies.
- Textbook dose-response: the bands where 252 added the most surge are exactly where completion rose most. At 4-5 km: multiplier 1.41 → 1.52, completion 0.770 → 0.890. At 9-10 km: similar surge bump bought a +0.145 jump.
- Bands where 252 barely changed the surge (12-16 km and beyond) show no lift at all.
- Correlation between how much surge rose and how much completion rose: r = +0.80, stable when weighted by sample size. No thin cells steering the line: lightest band ~1,100 searches, most between 2,000 and 5,000.
- Competitor gate cleared: NY was 5-33% cheaper than rivals across every band throughout, and drifted cheaper still over the rollout (from −10% to −18% on Auto Priority peak). No rider defection explains this lift.

**The ceiling.** Completion traces an inverted-U with surge: it climbs to around 1.4x, then falls above ~1.6x. The 250-to-252 move sat in the productive zone. The dial has room but it is narrow.

![Surge saturation: Auto Priority completion peaks near 1.4x then falls; Auto declines throughout](../02_Research/plots/fig2_saturation.png)

## Finding 2 — The headline +14.9% is mostly not the pricing. Three independent tests say so.

**Test 1: Dose-response runs backwards on mass Auto.** In the same 250-vs-252 peak comparison, 252 completes better in every band but does so with lower surge and a lower average fare (₹152 vs ₹154). When I bin by the surge actually applied within a fixed band, more surge tracks less completion: at 4-5 km, completion falls from 0.518 in the low-surge bin to 0.372 in the high-surge bin. The surge is reading market stress, not relieving it.

**Test 2: The placebo lights up.** A charge that only fires at peak cannot move hours where it never fired. Yet Auto completion rose just as much at night (0.335 → 0.437) and off-peak (0.430 → 0.522). Two things actually moved: a version swap buried in the rollout (v211 → v236/v250, which simply clears better at identical surge, 0.596 vs 0.558), and a supply expansion that predated the congestion logic.

**Test 3: Count, not ratio.** Auto searches dropped from 181k to 168k per day; completion-per-search climbed partly because fewer people were asking. The raw count of finished Auto rides began recovering before the charge shipped: 82,900/day in late May to 88,900 in early June, with the post-rollout window catching only the tail on a shrinking base.
