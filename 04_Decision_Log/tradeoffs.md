# 04 — Decision Log (append-only)

> Every strategic fork goes here: what I was choosing between, what I picked, and why.

---

### D-001 · Set up the PM OS before touching deliverables

Set up the four-folder workspace and the CLAUDE.md constitution before writing a single word of the answer. The rules that don't change session to session went in: no invented business constraints, two to three options at every crossroads, sequential approval gates between parts, a flat ban on generic PM jargon. The trade-off was scaffolding now (slower start) vs. jumping straight to analysis (faster, more drift). Chose scaffolding. The brief is long enough and has enough traps that without a shared frame the model would fill the gaps with generic product-manager defaults.

---

### D-002 · Whiteboard pass before opening any tool

Worked the problem by hand first, no tool open. The question I was answering: what has to be true for a completed ride to exist, and where in that chain is the congestion charge actually sitting? Sketched four stages — someone searches, gets a quote and accepts, a driver is dispatched, the ride completes without cancel — and the headline metric (completed/searches) telescopes across all four. Rough hypothesis after the whiteboard: driver cancellation is the biggest clean leak. It's within-NY, fully observable at Stage 3, and a pricing tool can only touch it at the margin if the cancellation motive is economic. Wrote this down before bringing anything to Claude Code.

---

### D-003 · Quick sanity check on the confounds before writing Part 1

The brief warned about the off-peak vs peak version assignment. Before ranking hypotheses I wanted to confirm the confound is actually in the data, not just stated in the brief. Ran a 5-minute check (01_sanity_check.py, 02_decompose_confound.py). It is real: v250/v252 runs almost exclusively in peak hours, v236 in off-peak/night. A naive 236-vs-250 comparison is measuring time-of-day, not pricing. The brief's own +14.9% reproduced immediately; then we confirmed the asserted mechanism — congestion charge raising driver supply — is absent on the mass Auto tier (surge moved 1.062 → 1.068). Reproduced the number, then showed the mechanism isn't there. Part 1 stays data-blind; the sanity check told me which confounds to name as Tests, not what the answers are.

---

### D-004 · Part 1 framing: rank pricing at H3; present fully data-blind

Two calls. First, where to rank pricing. Strong instinct to push it to H5 — it's a pricing brief, don't appear to be dodging the pricing question. Counter: the brief asks for ranking by size of impact, and Part 2 will show pricing is narrow. Chose H3 (medium): honest about the size, doesn't bury the lede. Second, whether to mention the sanity-check peek inside Part 1. Chose not to — Part 1 stays purely data-blind, and the prompt-trail flag belongs in Part 5 where the mechanism analysis lives. No conflict between the two.

---

### D-005 · First voice pass came back robotic; scrapped and recalibrated

First full draft of Part 1 read like a consulting slide deck: strict subject-verb-object on every sentence, comma-minimisation, each compound thought broken into a separate standalone statement. Technically clean but lifeless. The model had defaulted to a generic "PM document" register. Scrapped it. Pointed the model to my Substack as the voice reference and rebuilt the style rules from that: flowing argument-building paragraphs, claim then concrete example, semicolons and colons to join related thoughts, contrast structures for force, decisive stance throughout. Banned em dashes and AI tell-tales as hard rules. Rewrote Part 1 from scratch at this register. Voice held from that point forward.

---

### D-006 · MECE recut — one hypothesis was quietly the cause of another

First draft of Part 1 had five hypotheses that were not mutually exclusive. H4 (deadhead unpaid, driver cancels) was the structural cause behind H1 (driver cancellation), not a separate root cause. H3 (pricing) straddled Stage 2 (supply side, positive sign) and Stage 1 (rider side, negative sign) with opposite effects and needed to be split. Ran a MECE audit (logged in 02_Research/mece_check.md): the hypotheses were thematic, not nodal. Recut onto the funnel spine — one hypothesis per stage, congestion pricing split across Stage 2 (+) and Stage 1 (−), deadhead folded into H1 as its structural mechanism, second-order effects moved to an appendix. This resolved the exclusivity problem and sharpened the demand-defection risk that runs through Parts 2 and 4.

---

### D-007 · Nomenclature locked

Across the Part 1 draft, "nodes," "gates," and "stages" were all referring to the same funnel steps; three labels for two concepts. Fixed: funnel steps are Stage (0–3), causation checks are Test (1–5), a tier × distance × time-of-day cut is slice. Saved to CLAUDE.md section 3c. Small call, but mixed metaphors are a tell that the author doesn't own the framework — and the funnel spine is structural to every Part.

---

### D-008 · Multi-homing is structural, not exogenous

Initially put multi-homing under H5 (exogenous, external competition). Pulled it back out. NY is single-dispatch: one active ride per driver, no second ping while assigned. A visible concurrent better offer can only come from a competitor app, not from within NY. Multi-homing is the structural hole because rival apps can't see NY's busy flag — it's an information asymmetry baked into dispatch architecture, not a market condition NY passively faces. Moved it into H1 as the structural cause of the poach-cancel pattern; kept H5 for varying competitor-subsidy levels only. Test 5 now guards both Stage 1 (rider defection) and Stage 3 (driver poach).

---

### D-009 · Caught the model defaulting to commission-based pricing logic

Midway through Part 2 drafting, the model's competitor analysis started framing the problem as a take-rate optimisation: adjust the commission split to stay competitive, use per-trip margin headroom to fund driver incentives. Namma Yatri runs zero-commission. Rider fare equals driver take; there is no cut in the middle. The model had no strong prior for this product structure and kept reaching for the playbook baked into its training — most ride-hailing context in any training corpus is Uber-model, commission-based. I caught it because I expected it; this is the kind of prior mismatch I watch for by default with any agent. The fix wasn't to argue it out of the assumption each time it surfaced. It was to change how I worked with it at the branching and diagnosing stages: instructed it to surface the assumption and ask rather than run confidently in the wrong direction. The structural implication got folded into Part 2 as its own load-bearing section: zero-commission means the congestion charge is NY's only dial on driver pay, funded 1:1 from the rider, which is why it cannot outbid a competitor subsidy and why it saturates fast.

---

### D-010 · Ran the competitor gate before crediting any finding

Before staking any finding as a real win, ran the competitor check (03_competitor_defection.py) against the fare scrape. Two results: NY is 5–33% cheaper per km than rivals in every distance band (rider price-defection at Stage 1 ruled out), and NY drifted relatively cheaper across the rollout (Auto Priority peak −10% → −18%). The live competitor risk is driver poach at Stage 3, which price cannot answer under zero-commission. Short-trip gap narrowed from −33% to −23%, exactly where H3 said surge would bite. These guard rails had to come before the dose-response numbers meant anything.

---

### D-011 · Drafted under personas before finalising

Before finalising the Part 2 draft, ran it through four critic perspectives: a senior data analyst (do the numbers hold?), a product lead (does this change a decision?), a driver (does the framing match how I actually behave?), a Namma Yatri ops lead (what do I do with this on Monday?). The data analyst pass caught the fig5 mislabel — fare_sum/fare_n is average fare per trip within band, not price per km; a ₹600/km figure would have been absurd. The product lead pass flagged that F1 and F2 looked contradictory without an explicit reconciliation. The driver pass strengthened the deadhead framing in Part 3. The ops lead perspective is what drove the ≤5-line exec summary format. Each persona surfaces a different class of gap.

---

### D-012 · Two reputation-grade findings staked; alternatives ruled out

Ran Test 4 (04_doseresponse_placebo.py). Two findings survived the full ladder. F1 — narrow real win: Auto Priority peak v252 has a clean +0.80 dose-response, competitor gate clears, bounded by an ~1.5x saturation ceiling (within-band inverted-U). F2 — headline fails: the +14.9% is not the pricing. Auto surge vs completion is inverse (corr −0.72), the placebo lights up (off-peak rose as much as peak), and raw Auto completed rides fell post-rollout (16.9k → 15.9k); the ratio rose only on a shrinking search base. F1 and F2 coexist: v252 converts a higher fraction of a collapsing base. Both stated in the draft without softening either.

---

### D-013 · Part 3 experiment lever: re-route the congestion rupee as named deadhead pay

First experiment framing was pickup compensation as a new rider charge. Reframed: not a new charge — re-route the rupee the rider already pays and make it legible to the driver as deadhead pay, with net-of-deadhead earnings shown pre-accept on the offer card. Same money, one shared honest story to both sides. Root cause: driver accepts blind to the deadhead distance, app reveals it only after accept, and that is when the cancel happens. Two honesty guardrails added: (1) the whole premise is contingent on Step 0, an audit of what the live offer card actually shows; (2) congestion is area-based, deadhead is trip-based, and they only fund each other in busy zones, so the first test is scoped to peak hours where they align.

---

### D-014 · Verified the no-quote rider is structurally invisible in the data

The claim in Part 3.3 — rider gets no quote at the offered price and silently leaves — needed to be grounded against the schema or explicitly flagged as unobservable. Checked DATA_DICTIONARY.html. Three separate reasons it's invisible: no IDs so no cross-platform link; fare quantiles are on completed rides only so the price a non-converting rider saw is unrecorded; can't cleanly count the no-match population at all. Also surfaced a funnel-count caveat that carries to Part 5: rider_acceptances (Auto 9.5M) exceeds searches (Auto 6.36M) because of retries, so acc/search sits above 1 — an amplification, not a conversion rate. completed/searches, used throughout, is unaffected. Tightened Part 3.3 prose and flagged both gaps for Part 5.

---

### D-015 · Defended lever: supply-shaping, staged before committed rides

Part 4 lever choice. Committed/reserved rides is the most complete structural fix but high-friction: it penalises cancellation defaults, and you can't guarantee a rider a slot without first fixing driver supply and incentives — the prerequisite doesn't exist yet. Supply-shaping (predictive repositioning) is zero-cost, uses data NY already owns, and builds the active-driver density that committed rides needs to work. New analysis (06_supply_and_defection.py) confirmed demand is predictable (weekday hourly search CV median 0.26, midday CV 0.05–0.13, recurring AM/PM peaks) and the completion leak is worst exactly at the predictable evening peak (comp/search 0.37 at 18h, cancels at daily high). Sequencing is the strategy: supply-shaping thickens the base now for free, committed rides graduates the reliable pairs once density exists.

---

### D-016 · Part 4 recut as a MECE demand/supply/match option space

First draft of Part 4 riffed on the brief's example levers. Brief explicitly rewards inventing beyond them. Recut onto a MECE spine: a completed ride needs demand, supply, and a match that holds, and every lever moves exactly one. Walked each column with persona, JTBD, pain point, and inventive levers — intent-ahead booking, no-quote fallback captured as signal, go-online nudge, back-haul intelligence, proximity-first dispatch. Convergence logic built into the structure: demand is not the scarce input at peak, match-structure levers need supply density first, so supply-positioning is where binding constraint × data NY already owns × zero-cost all intersect. The map funnels to supply-shaping; the rest become a sequenced roadmap rather than a competing menu.

---

### D-017 · Part 5: four critiques staked; prompt-trail flag delivered

Read the attached AI analysis (verdict: success on every metric, ship 100%, expand to Delhi/Kolkata). Selected four critiques from roughly eight candidate flaws, each tied to a concrete ship/don't-ship decision rather than an abstract statistical objection. (1) The headline is the confound plus falling denominator plus placebo, not the pricing. (2) The asserted supply mechanism is absent on Auto — surge moved 1.06 → 1.07 — and Finding 5 "supply rose from the charge" directly contradicts Finding 2 "fare held flat." (3) "AP loves it" confuses ratio with rides (AP completed fell), supply with driver sentiment, and ignores no-quote exits. (4) "Proven at scale, ship 100%" inverts an outcome-dependent ramp into causal proof — a process error, not a measurement error, and the most dangerous of the four. Reproduced the +14.9% exactly in the opening, then showed the mechanism is absent: that is the prompt-trail flag.

---

### D-018 · Director-review pass: verified three objections before deciding how to respond

Six objections came back from the Director-persona critique. Ran 07_verification_pass.py to check three against the data before deciding whether to soften or harden the draft. The AP thin-cell objection was refuted — lightest band is n ~1,131, correlation is +0.80 weighted, unweighted, and dense-band-only; Finding 1 gets harder, not softer, and the n's are now in the text as armor. The Auto-completed-rides objection was confirmed — +3.2% genuine growth, not pure denominator shrink; conceded it, reframed from "denominator shrank" to "+14.9% overstates a small real gain." The unnamed-placebo-cause objection was resolved — two mechanisms: a version-composition swap in the off-peak/night zone (newer versions clear better at flat surge, a matching gain not a congestion gain) and a flat cancel rate at peak (.325 → .325) while the search base thinned. Both named in the draft. Supply-shaping kept as defended lever, reframed as a sequenced bet downstream of the geo instrumentation Part 5 demands.

---

### D-019 · Part 1 director pass: one edit made, rest banked as interview prep

Director review of Part 1 confirmed the pre-data ranking held: cancel/ride 0.315, split 53% driver / 47% user on Auto, flips to 47/53 on Auto Priority. H1 vindicated; the Section 3 reflection predicted Part 2 before the data was opened. One edit made: added a one-line caveat that the funnel is a decomposition, Stage 1 is retry-inflated (acc/search can sit above 1, not a clean conversion rate), and the real measured leaks are Stage 2 and Stage 3. Phrased data-blind since the caveat is knowable from the data dictionary, not from the findings. Everything else — the 50/50 split nuance, the MECE axis note, the vindication pointer — deliberately deferred. Part 1's value is "called it before opening the data"; retrofitting findings destroys that credibility. Banked as interview talking points in 05_Interview_Prep/prep_notes.md.
