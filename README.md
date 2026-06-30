# Namma Yatri — PM Take-Home

## The problem

Leadership's read going into this: completed auto rides per day in Bangalore slipped through May, then ticked up after the congestion-based pricing shipped two weeks ago. The plan was to roll `v250/v252` to 100% of Bangalore autos and expand to Delhi and Kolkata.

**Our job: pressure-test that belief before the ship decision.**

Namma Yatri is structurally different from Uber or Ola in ways that change what every lever actually does. It runs zero-commission — drivers pay a small flat subscription, NY takes nothing per fare, and competitors fund bonuses by burning investor money that NY won't. That means the congestion charge is NY's only dial on driver pay: it is funded 1:1 from the rider, cannot outbid a competitor subsidy, and saturates fast. The other constraint is the stale government tariff — a distance-only meter with almost no time-of-day component, so the 9am peak and the 2pm empty-road get priced the same. At peak, the fare can sit below a driver's real cost when you factor in the unpaid deadhead to reach the rider. That is the specific gap the congestion charge is trying to close.

The pricing experiment was not a clean A/B test. Version assignment was observational, gated by zone and time-of-day, and outcome-dependent (winners ramped toward 100%, which removes any control). Critically, `v250/v252` ran almost exclusively in peak hours while the baseline `v236` ran mostly off-peak and at night — so a naive before/after comparison is measuring time-of-day, not pricing. The one clean head-to-head left in the data is `v250` vs `v252` inside peak hours, same tier, same distance bands.

## The thesis

The congestion charge does real work in exactly one slice: Auto Priority at peak, where the dose-response correlation across distance bands is r = +0.80. On the mass Auto tier it runs inverse (r = −0.72): more surge, less completion. The headline +14.9% is mostly a shrinking search base, demand that was already recovering before the charge shipped, and an off-peak version swap that had nothing to do with congestion pricing. The real leaks are the driver cancelling over an unpaid deadhead he couldn't see before accepting, and the rider who gets no quote at the offered price and silently opens another app — neither of which is a problem a price multiplier fixes.

---

## The solution

The full written response is split across two folders:

**[`03_Insights/compact/`](03_Insights/compact/)** — The submission-ready version of each Part, condensed for the PDFs. Lead-with-the-verdict structure; this is the version that accompanies the PDF.

**[`03_Insights/verbose/`](03_Insights/verbose/)** — The uncut internal docs: the complete reasoning behind every finding, every alternative ruled out, and every decision. Longer and more granular than the submission layer; this is where the thinking lives.

Both folders contain the same eight documents:

| File | What it covers |
|---|---|
| `Part1_Framing.md` | Five ranked hypotheses (data-blind), the four-stage funnel, and a five-test causation ladder. Driver cancellation leads; congestion pricing is H3, not H1. |
| `Part2_DidPricingWork.md` | Two reputation-grade findings: the real Auto Priority peak win (r = +0.80) and the headline failure diagnosis. Competitor guard, dose-response, placebo, and raw count all run. |
| `Part3_PeopleAndBehaviour.md` | The driver's offer-card blindness, the deadhead-pay experiment design, and the no-quote rider who's structurally invisible in the data. |
| `Part4_TheConstraint.md` | A MECE demand/supply/match option space for growing rides under zero-commission, and the defended lever: supply-shaping as the zero-cost first move, committed rides as the sequenced endgame. |
| `Part5_StressTest.md` | Four critiques of the attached AI analysis, each tied to a ship/don't-ship decision. The prompt-trail flag: we reproduced the +14.9%, then showed the mechanism is absent. |
| `ExecSummary.md` | The ≤5-line ops + exec summary: do / stop-hold / one number to watch. |
| `HowIWorked.md` | How the work was structured: the PM OS, the sequencing, and the human/AI division of labour. |
| `Spine.md` | The narrative connective tissue tying all five parts into one coherent argument. |

---

## The analysis

`02_Research/` contains 12 reproducible Python scripts. Each one builds every number it cites from the raw cube — no notebooks, no hardcoded outputs. The investigation runs in sequence: confirm the confounds, close the competitor guard, run the causal tests, then dig into the specific questions the draft raised.

| Script | Question it answers |
|---|---|
| [`01_sanity_check.py`](02_Research/01_sanity_check.py) | Replicate the AI's +14.9%. Are the brief's confounds actually in the data? |
| [`02_decompose_confound.py`](02_Research/02_decompose_confound.py) | Simpson's paradox check — does the lift survive when time-of-day is held fixed? |
| [`03_competitor_defection.py`](02_Research/03_competitor_defection.py) | Competitor guard (Test 5): is NY above-market? Could riders or drivers defect? |
| [`04_doseresponse_placebo.py`](02_Research/04_doseresponse_placebo.py) | Dose-response and placebo (Test 4): does more surge actually cause more completions? |
| [`05_plots.py`](02_Research/05_plots.py) | The five evidence figures embedded in Part 2. |
| [`06_supply_and_defection.py`](02_Research/06_supply_and_defection.py) | Is demand predictable enough to shape supply against it? Where does the loop leak by hour? |
| [`07_verification_pass.py`](02_Research/07_verification_pass.py) | Director-review robustness check on the three most contestable findings. |
| [`08_build_explorer_json.py`](02_Research/08_build_explorer_json.py) | Exports dose-response evidence as JSON for the interactive slice explorer. |
| [`09_cancellation_breakdown.py`](02_Research/09_cancellation_breakdown.py) | Driver vs rider cancel split by tier, hour, and distance — validates the deadhead hypothesis. |
| [`10_weekly_trend.py`](02_Research/10_weekly_trend.py) | Week-on-week trend: step-change at rollout or smooth recovery that predates it? |
| [`11_retry_analysis.py`](02_Research/11_retry_analysis.py) | The acc/search > 1 inflation — retry volume as a proxy for structurally unobservable demand. |
| [`12_peak_supply_gap.py`](02_Research/12_peak_supply_gap.py) | Gap score by hour (demand × unmet fraction) — names the target window for supply-shaping. |

To run with the original data in place:

```bash
pip install pandas numpy matplotlib
python3 02_Research/01_sanity_check.py
python3 02_Research/04_doseresponse_placebo.py
python3 02_Research/05_plots.py
```

---

## Repo structure

| Path | What's in it |
|---|---|
| [`claude.md`](claude.md) | The operating constitution: product context, rules of engagement, writing voice, data-handling rules. |
| [`01_Foundation/`](01_Foundation/) | Problem statement of record — the shared context written before any data was opened. |
| [`02_Research/`](02_Research/) | Analysis scripts, findings markdowns, and figures. |
| [`03_Insights/`](03_Insights/) | The written response, in `compact/` (submission) and `verbose/` (full reasoning). |
| [`04_Decision_Log/tradeoffs.md`](04_Decision_Log/tradeoffs.md) | Append-only audit trail: 19 entries, every fork, the options, the choice, and the why. |

---

## A note on the data

The original brief, data dictionary, pricing experiment log, attached AI analysis, and the raw `data/*.csv` are Namma Yatri's own materials and their real (de-identified) ride data. They are intentionally excluded from this repo so it is safe to host publicly. Everything here — including the aggregated figures — is derived and presented solely for this assessment.
