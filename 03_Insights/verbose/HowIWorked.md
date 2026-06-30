# How I worked

*The brief asks for the prompt trail and one place I pushed past the AI. Here is how I actually ran this, what I built to keep the AI honest, and the moments my judgment overrode its first answer.*

## I didn't prompt an AI; I ran one

A model computes a funnel in two minutes. That was never the test, and pasting its first answer is how you score poorly, because that answer is generic and, on this brief specifically, wrong. So I treated the AI the way I would treat a fast, tireless analyst who has no judgment and no skin in the game: I gave it a constitution, a workspace, and a standing instruction to argue with me.

The constitution was a single operating file the AI had to read at the start of every session. It set hard rules that are easy to say and hard to hold: make zero business assumptions and ask when a product decision is ambiguous; present two or three real options at every crossroad with explicit trade-offs and let me choose; never advance to the next Part without my explicit approval; and validate every hypothesis against the data before we "stake our reputation" on it. It also fixed the nomenclature so the work couldn't drift into mixed metaphors: funnel steps are always a **Stage**, causation checks are always a **Test**, a tier-by-distance-by-time cut is always a **slice**. One plain noun per concept, reused everywhere.

The workspace was four folders that separate thinking from output: a Foundation of record, a Research folder where every number is a reproducible Python script, the PRD answers themselves, and an append-only Decision Log that captured every strategic fork, the options on the table, the choice, and the why. Eighteen entries by the end. That log is the real artifact of how this was made, and it is in the repo unedited.

## The prompt trail, curated to the moves that mattered

The raw session was long and had dead ends; nobody benefits from that transcript. These are the directives that actually steered the work, in order. Each one maps to a Decision Log entry you can open and check.

1. **"Frame before you touch the data, but let me sanity-check the confounds first."** The brief says don't open the data for Part 1. I went a half-step further: a five-minute validation run to confirm the brief's confounds were real before I ranked hypotheses around them, then wrote Part 1 fully data-blind so the framing stayed pure. Grounding the framing without contaminating it.

2. **"Rank by where in the chain the lever acts, not by theme."** Completed rides are the last survivor of a four-stage chain. I forced the hypotheses onto that spine so they were mutually exclusive and exhaustive by construction, and split the congestion charge across two of them, because the same rupee that pulls a driver in at one stage pushes a price-sensitive rider out at another.

3. **"This is a pricing brief; don't look like you're dodging the pricing question."** A judgment call on positioning: keep driver cancellation as the lead hypothesis, but answer the pricing question head-on at a credible middle rank rather than burying it at the bottom. Bold but not evasive.

4. **"That draft reads like a robot. Here's my actual voice."** The first style I locked was strict subject-verb-object, and it came out mechanical. I scrapped it, recalibrated against my own published writing, and rewrote everything in flowing, argument-building prose. Two more passes after that to settle the density. The voice is mine, deliberately.

5. **"Run a MECE check on your own hypotheses."** It found my first cut wasn't clean: one hypothesis was the cause of another, one spanned two stages. I recut the whole thing onto the funnel spine and added a second-order-effects appendix for the cross-cutting risks.

6. **"Run Part 1's own five-test ladder on the data; don't write a before-and-after."** Part 2 wasn't approached as "did pricing work" cold. It was the same ladder Part 1 defined, run slice by slice, tracking the raw completed count over the seductive ratio, with the competitor gate run first to close the defection question before crediting any slice.

7. **"Plot it, and tell me whether zero-commission changes the read."** That second question turned an empirical finding into a structural one. Because NY is zero-commission, the rider's fare *is* the driver's take, so the congestion charge is the only dial NY has on driver pay and it hits rider price-sensitivity the instant it moves. That is the structural floor under everything, and it pre-loaded the Part 4 constraint.

8. **"Invent beyond the brief's example levers."** Part 4's first menu just riffed on the brief's own examples. I pushed for a MECE decomposition of the whole marketplace, demand-supply-match, walked each along its persona and job-to-be-done, then let the data funnel the map down to one defended lever instead of presenting a brainstorm.

9. **"Give me a Product-Director critique of the whole thing, then act on it."** Six objections came back. I wrote a verification script to test them against the data rather than just accepting them, which produced the correction below.

## Where I pushed past the AI

Two moments, and the second is the one I'm proudest of.

The headline catch. The attached AI analysis concludes the rollout was a success and says to ship it to 100% and to two more cities. I reproduced its number exactly, +14.9% on completion-per-search, to the decimal, so there was no hiding behind a computation dispute. Then I showed that the correct number is the wrong evidence: the same lift appears in the no-surge night and off-peak hours where the charge never fired, the ratio's denominator was falling because fewer people were searching, and the raw count of finished rides shows the recovery beginning *before* the charge shipped. On the mass tier the applied surge moved six rupees on a ₹150 fare, which cannot summon a supply wave, and the analysis even contradicts itself: it celebrates that the fare "barely moved" while crediting that same fare with raising supply. A correct calculation producing a wrong recommendation is the whole point of Part 5.

The catch on myself. When I stress-tested my own Finding 1, I worried its dose-response might be riding on thin, noisy premium-tier cells, the kind of objection that quietly kills a finding. So I wrote a script to check the sample sizes instead of guessing. It refuted my own worry: every band in that comparison carried a real sample, the correlation held at +0.80 unweighted, search-weighted, and dense-cells-only. The honest move was not to soften the finding but to *harden* it by publishing the sample sizes, and to concede in the same pass that a different objection had teeth, that the mass-tier Auto count did post a real, if small, +3.2% gain I had been too quick to wave away as pure denominator. I corrected the analysis against itself, in both directions, on the evidence. That is the bar I was holding the AI to, so it is the bar I held myself to.
