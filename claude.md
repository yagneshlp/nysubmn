# claude.md — PM Operating System

> Static operating instructions for the Namma Yatri PM take-home. Read at the start of every
> working session. This file is not memory — it holds rules and context that don't change.

---

## 1. Product context (ground truth — do not infer from training data)

**What Namma Yatri is:**
Namma Yatri is a zero-commission, open-source auto-rickshaw aggregator operating primarily in
Bengaluru, with presence in Mysuru and a few other Indian cities. It runs on the ONDC (Open
Network for Digital Commerce) protocol. The codebase is FOSS.

**The commission model distinction — read this carefully:**
NY runs zero-commission. Rider fare equals driver take; there is no platform cut in the middle.
This is structurally different from Uber, Ola, and Rapido, which take a percentage commission and
can independently subsidise driver payouts or offer rider discounts from the margin. Under
zero-commission, the congestion charge is NY's only dial on driver pay, and it is funded 1:1
from the rider. The model cannot outbid a competitor subsidy. Any analysis that drifts toward
commission-split optimisation, take-rate adjustments, or margin-funded incentives is wrong by
construction — surface the assumption and stop.

**Geography and peak-hour context:**
Bengaluru has pronounced AM and PM rush peaks (roughly 08–11 and 16–20) driven by IT corridor
commuter patterns. The congestion pricing experiment is specifically a response to these peaks.
Off-peak hours (midday, late night) are structurally different supply-demand environments.

**What the data does not have (geo constraints):**
The ride cube contains no geographic data. There are no pickup or drop coordinates, no zone
identifiers, no supply-density-by-area signals, no neighbourhood-level demand heat. Distance is
available only as bucketed ranges. Any claim about geographic supply positioning, hot-zone
pre-positioning, or area-level demand forecasting is a strategy recommendation that requires
instrumentation NY does not yet have in this dataset — state it as such.

---

## 2. Rules of engagement

- **Zero assumptions on the business.** When a product decision is ambiguous, ask. Never invent
  business constraints. Analytical defaults on the data are fine if stated explicitly.
- **Options at every crossroads.** Two to three viable paths with explicit trade-offs (speed vs
  scale, UX vs engineering effort, rigour vs time). User chooses.
- **The bar.** No fluff, no generic PM jargon. Ruthless prioritisation, systemic thinking, deep
  grasp of two-sided marketplace dynamics. A tight partial beats a sprawling whole.
- **Sequential execution.** Do not advance to the next Part until the user explicitly approves
  the current one.
- **Show the work.** Every hypothesis tested gets validated against data before being staked.
  Flag at least one place where the analysis corrected or pushed past the AI's default.

---

## 3. Writing style (applies to all deliverables and docs)

Write in the user's voice, calibrated from their Substack. The target is flowing, decisive,
argument-building prose — not choppy strict-SVO. Coherence and flow win over mechanical rules.

- Build a claim, then prove it with concrete examples and analogies. Ground every abstraction
  in something vivid and specific.
- Write medium-length sentences that connect ideas. Use semicolons and colons to join related
  thoughts. Use commas freely when they serve flow. A short punchy line is for deliberate
  emphasis only, never the default rhythm.
- Use contrast structures for force ("These weren't just X; they were Y").
- Stay decisive and authoritative. Take a stance. First-principles framing.
- No em dashes. Ever. Use semicolons, colons, or periods instead.
- No AI tell-tales ("Certainly!", "In conclusion," "As an AI"). Jump to the point. Never restate
  the question.
- Avoid the failure mode: strict Subject-Verb-Object on every line, comma-minimisation, breaking
  every compound into separate standalone statements. That reads robotic.
- Use a list only when the brief demands one or for a true sequential procedure. Even inside a
  ranked list, write each item as a flowing paragraph.
- Tone: natural and plain-spoken, like a sharp PM talking to a smart colleague. Plain everyday
  words over stiff ones. Light conversational setups and the occasional contraction are fine.
  A notch warmer than a formal report, never childlike.

---

## 4. Nomenclature (hold consistent across all Parts)

- Funnel steps: **Stage** (Stage 0 demand → Stage 1 rider conversion → Stage 2 supply quotes →
  Stage 3 honour). Never "node."
- Causation checks: **Test** (Test 1–5). Never "gate."
- A tier × distance band × time-of-day cut: **slice**. Use the brief's word verbatim.
- One plain noun per concept, reused everywhere. No mixed metaphors.

---

## 5. Data handling rules

The data is a pre-aggregated cube, not per-trip rows.
Grain: `date × is_weekend × hour_bucket × service_tier × pricing_version × distance_bucket`.

**Additive columns** (searches, rides, completed, cancelled, `*_sum`, `*_n`): sum freely, then
compute rates. **Quantile columns** (`*_p25/p50/p75/p90`): frozen per cell — never average a
median across cells. For cross-cell central tendency, rebuild from additive columns
(e.g. `completed_fare_sum / completed`).

**Confounds to respect:** version assignment is observational, gated by zone and time-of-day,
and outcome-dependent (winners ramped fast). v250/v252 run mainly in peak (~08–11, 16–20);
baseline v236 runs mainly off-peak/night. Naive 236-vs-250 = off-peak-vs-peak, not pricing.
The clean head-to-head is 250 vs 252 inside peak. Distance is not confounded.

**Never blend Auto and Auto Priority** into one number.

Competitor scrape routes skew long (median ~16 km); compare within `distance_bucket`.
Respect sample size — thin cells are noisy.

**Unobserved population:** riders who got no quote or an expensive quote and silently left are
not in the data. No IDs means no per-rider or per-driver tracking, no earnings per hour, no geo.
