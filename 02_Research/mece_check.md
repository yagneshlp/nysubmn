# MECE Check on the Part 1 Hypotheses

*Question: are H1–H5 mutually exclusive and collectively exhaustive, and what 2nd/3rd-order effects do they miss?*

## The MECE spine: the funnel is an identity, so use it as the test

Completed rides decompose uniquely into multiplicative stages. Nothing can drive completed rides
without moving one of these terms. This is MECE by construction.

```
completed = searches × (acc/search) × (ride/acc) × (1 − cancel rate)
            ──────     ──────────     ─────────     ──────────────
            Node 0      Node 1         Node 2        Node 3
            demand      rider gets a   a driver      booking is
            volume      usable quote   quotes &      honoured, not
                        & accepts      matches       cancelled
```

Node 3 splits further, and the split matters: `cancelled_by_driver`, `cancelled_by_user`,
`cancelled_other`. These are different failures with different fixes.

## Map the hypotheses onto the spine

| Hypothesis | Node it acts on | Direction |
|---|---|---|
| H1 driver cancellation | Node 3 (driver) | the leak itself |
| H2 demand volume | Node 0 | sets the ceiling |
| H3 price adequacy | Node 2 (+) **and** Node 1 (−) | pulls supply, pushes price-sensitive riders out |
| H4 deadhead / matching | Node 2 **and** Node 3 | upstream cause |
| H5 exogenous | shifts the inputs to all nodes | confounder |

## Verdict 1: they are NOT mutually exclusive

Three overlaps break exclusivity, and each is a real reasoning flaw, not a labelling nitpick.

**H4 is the cause of H1, not a sibling of it.** Deadhead distance is *why* the driver cancels. I
listed the symptom (cancellation) and its mechanism (deadhead) as two parallel hypotheses. They are
one causal chain. The honest structure is: deadhead economics → driver declines or cancels → Node 3
leak.

**H3 acts through H1's node, and against H2's.** Price is one input to the same driver accept-and-
honour decision H1 describes, so H3's upside and H1 live at the same place. H3 also has a downside
that lands in Node 1 (a higher fare makes the rider reject the quote). So H3 is not a clean
standalone lever; it is a two-signed force that touches two nodes already named.

**Net:** the list is organised by theme (supply, demand, price, matching, exogenous), not by node.
Themes overlap. Nodes do not.

## Verdict 2: they are NOT collectively exhaustive

Mapping to the spine exposes a thin spot at **Node 1 and the rider side of Node 3**. The current
five are supply-and-price heavy. Three real drivers have no first-class hypothesis:

**M1 — The no-quote / rejected-quote moment (Node 1 conversion, not Node 0 volume).** H2 covers how
many riders *search*. It does not cover the rider who searched, got nothing usable, and left. That
is a conversion failure driven by supply liquidity, not a demand-volume failure. It is also the
single moment the data cannot see directly, which makes it the most dangerous gap.

**M2 — Rider-side cancellation (`cancelled_by_user` in Node 3).** A rider cancels because the ETA is
too long or a competitor quoted cheaper. This is a distinct leak from driver cancellation, with a
distinct fix, and H1 silently folds it in.

**M3 — Supply liquidity as a stock, not a per-trip choice.** The number of drivers online in a zone
sets the deadhead for *every* trip in that zone at once. H1 and H4 treat the driver's decision one
trip at a time. The thickness of the market is a level above that, and price is one of the things
that moves it.

## Second and third-order effects the flat list misses

**E1 — Supply spillover (2nd order, and it threatens our own test).** Peak surge pulls more drivers
online. Those drivers shorten pickups and complete more trips nearby, including trips that were not
surged, and including the shoulder hours just after peak. This is the mechanism that can make
off-peak completion rise with no off-peak surge. It is a direct threat to the placebo gate in Part
1, Section 2: a flat-looking placebo could be contaminated by spillover from the adjacent peak. We
must check the placebo in slices that are spatially and temporally far from any surge, not merely
off-peak.

**E2 — Demand learning (3rd order).** Riders who get surged repeatedly learn the timing and either
shift their trip or stop searching at peak. That destroys peak demand slowly and invisibly inside a
five-week window. A short study will score this as "fares flat, completion up" while the demand base
quietly erodes.

**E3 — Cross-platform multi-homing (2nd order).** The driver allocates his hour by comparing NY's
surge to the competitor's surge in real time. NY's lever strength is not absolute; it is relative to
whatever the competitor is doing that same hour. This is why the competitor fare check is a gate,
not a footnote.

**E4 — Composition shift (2nd order).** Surge filters which trips complete. If it suppresses short
unprofitable trips and passes longer ones, average fare and completion both move for mix reasons,
not behaviour reasons. We must read completion within a fixed distance band, never pooled.

**E5 — Attribution gaming (3rd order).** A driver accepts then stalls to force the rider to cancel,
which flips the failure from `cancelled_by_driver` to `cancelled_by_user`. The Node 3 split can look
like it improved on the driver side while nothing real changed. This connects directly to Part 3's
gaming question.

## What I would change in Part 1

Re-cut the hypotheses onto the funnel spine so they are mutually exclusive by node, fold H4 into H1
as its named cause, split H3 into its two signs, and add M1/M2 so the rider side is represented. Keep
E1–E5 as a short "second-order effects and risks to the test" block, because E1 in particular forces
a stronger placebo design.
