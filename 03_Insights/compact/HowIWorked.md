# How I worked

## I started with whiteboarding the context and mapping a customer journey, noting assumptions, questions and hypotheses before getting to an AI agent

### Tool of choice: Claude Code — multiple models for different purposes
Opus for planning, Sonnet for execution

LLM roundtable was employed on multiple occasions to get different perspectives; used Gemini Pro over web to counter-propose and critique.

## Setting up the workbench

 I treated the AI as a fast, tireless analyst with no judgment and no skin in the game: I gave it a constitution, a workspace, and a standing instruction to argue with me. also a persona at times to provide a direction of thought.

The constitution was a single operating file with hard rules: zero business assumptions; present 2-3 real options at every fork with explicit trade-offs and let me choose; never advance to the next Part without explicit approval; validate every hypothesis against the data before staking a reputation on it. It also fixed the nomenclature so the work could not drift: funnel steps are always a **Stage**, causation checks always a **Test**, a tier-by-distance-by-time cut always a **slice**.

The workspace was four folders separating thinking from output: Foundation (context of record), Research (every number a reproducible Python script), PRD answers, and an append-only Decision Log capturing every strategic fork, the options, the choice, and the why. Eighteen entries by the end. The log is in the repo unedited.

## The prompt trail

The directives that actually steered the work, in order. Each maps to a Decision Log entry you can open and verify.

1. **"Frame before you touch the data, but sanity-check the confounds first."** Confirmed the brief's confounds were real before ranking hypotheses around them, then wrote Part 1 fully data-blind so the framing stayed pure.
2. **"Rank by where in the chain the lever acts, not by theme."** Forced hypotheses onto the four-stage funnel spine so they are mutually exclusive and exhaustive by construction; split the congestion charge across two stages because the same rupee pulls a driver in at one and can push a rider out at another.
3. **"This is a pricing brief; don't look like you're dodging the pricing question."** Kept driver cancellation as the lead hypothesis but answered pricing head-on at a credible middle rank rather than burying it.
4. **"That draft reads like a robot. Here's my actual voice."** Scrapped strict subject-verb-object, recalibrated against my own published writing, rewrote in flowing argument-building prose. Two more passes after that.
5. **"Run a MECE check on your own hypotheses."** Found the first cut was not clean: one hypothesis was the cause of another, one spanned two stages. Recut everything onto the funnel spine.
6. **"Run Part 1's five-test ladder on the data; don't write a before-and-after."** Applied the ladder slice by slice, tracking raw completed counts over the seductive ratio, with the competitor gate run first.
7. **"Plot it, and tell me whether zero-commission changes the read."** The second question turned an empirical finding into a structural one: under zero-commission, the rider's fare is the driver's take, so the congestion charge is the only dial NY owns on driver pay and it hits rider price-sensitivity the instant it moves.
8. **"Invent beyond the brief's example levers."** Pushed for a MECE decomposition of the whole marketplace (demand-supply-match), walked each along its persona and job-to-be-done, then let the data funnel the map to one defended lever instead of presenting a brainstorm.
9. **"Give me a Product-Director critique of the whole thing, then act on it."** Six objections came back. I wrote a verification script to test them against the data rather than just accepting them, which produced the correction below.

## Where I pushed past the AI

**The headline catch.** The attached AI analysis says to ship to 100% and two more cities. I reproduced its +14.9% exactly, to the decimal, so there was no hiding behind a computation dispute. Then I showed the correct number is the wrong evidence: the same lift appears in hours where the charge never fired, the denominator was shrinking, and raw rides began recovering before the charge shipped. The analysis even contradicts itself: it celebrates that the fare "barely moved" while crediting that same fare with raising supply. A correct calculation producing a wrong recommendation is the whole point of Part 5.

**The catch on myself.** When I stress-tested Finding 1, I worried its dose-response was riding on thin, noisy premium-tier cells, the kind of objection that quietly kills a finding. So I wrote a script to check sample sizes instead of guessing. It refuted my own worry: every band carried a real sample, the correlation held at +0.80 unweighted, search-weighted, and dense-cells-only. The honest move was not to soften the finding but to harden it by publishing the sample sizes, and to concede in the same pass that a different objection had teeth: the mass-tier Auto count did post a real, if small, +3.2% gain I had been too quick to wave away as pure denominator. I corrected the analysis against itself, in both directions, on the evidence. That is the bar I was holding the AI to, so it is the bar I held myself to.
