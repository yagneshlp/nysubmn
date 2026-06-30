# Namma Yatri — PM Take-Home

This is the full working repo for a PM take-home on Namma Yatri's congestion-based pricing experiment: the submitted deliverables, the analysis scripts that built every number in them, a decision log, and the AI operating constitution used throughout. Start with the PDFs in [`05_Solution/`](05_Solution/); everything else is the working layer underneath.

---

## What's here

| Path | What's in it |
|---|---|
| [`05_Solution/NammaYatri_PM_Solution.pdf`](05_Solution/NammaYatri_PM_Solution.pdf) | Full written response: all five parts, the analysis, and the recommendations. |
| [`05_Solution/NammaYatri_PM_AIProcessOutline.pdf`](05_Solution/NammaYatri_PM_AIProcessOutline.pdf) | One-page anatomy of how AI was used: which stages were human-led, where the model drifted, how the working system was structured. |
| [`02_Research/`](02_Research/) | 12 Python scripts that build every cited number from the raw cube. No notebooks, no hardcoded outputs. |
| [`04_Decision_Log/tradeoffs.md`](04_Decision_Log/tradeoffs.md) | Append-only audit trail: 19 entries, every fork, the options, the choice, and the why. |
| [`01_Foundation/`](01_Foundation/) | Problem statement written before any data was opened. |
| [`CLAUDE.md`](CLAUDE.md) | The operating constitution used to direct the AI: product context, data-handling rules, writing voice. |

---

## Analysis scripts

| Script | Question |
|---|---|
| [`01_sanity_check.py`](02_Research/01_sanity_check.py) | Replicate the AI's +14.9%. Confirm the confounds are real. |
| [`02_decompose_confound.py`](02_Research/02_decompose_confound.py) | Simpson's paradox check: does the lift survive with time-of-day held fixed? |
| [`03_competitor_defection.py`](02_Research/03_competitor_defection.py) | Competitor guard: is NY above-market on fares? |
| [`04_doseresponse_placebo.py`](02_Research/04_doseresponse_placebo.py) | Dose-response and placebo: does more surge actually cause more completions? |
| [`05_plots.py`](02_Research/05_plots.py) | The five evidence figures embedded in Part 2. |
| [`06_supply_and_defection.py`](02_Research/06_supply_and_defection.py) | Where does the supply-demand loop leak by hour? |
| [`07_verification_pass.py`](02_Research/07_verification_pass.py) | Robustness check on the three most contestable findings. |
| [`08_build_explorer_json.py`](02_Research/08_build_explorer_json.py) | Exports dose-response data as JSON for the interactive slice explorer. |
| [`09_cancellation_breakdown.py`](02_Research/09_cancellation_breakdown.py) | Driver vs rider cancel split by tier, hour, and distance. |
| [`10_weekly_trend.py`](02_Research/10_weekly_trend.py) | Step-change at rollout, or smooth recovery that predates it? |
| [`11_retry_analysis.py`](02_Research/11_retry_analysis.py) | Retry volume as a proxy for structurally unobservable demand. |
| [`12_peak_supply_gap.py`](02_Research/12_peak_supply_gap.py) | Gap score by hour: names the target window for supply-shaping. |

To run with the original data in place:

```bash
pip install pandas numpy matplotlib
python3 02_Research/01_sanity_check.py
```

---

*The raw data, brief, and pricing experiment log are Namma Yatri's materials and are excluded from this repo. Everything here is derived and presented solely for this assessment.*
