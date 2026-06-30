# Namma Yatri — PM Take-Home

**Did the new congestion pricing actually work?** A slice-level pressure-test of the rollout, the people behind the funnel, and the one lever that grows completed rides without a subsidy or a commission.

The thesis in one line: the congestion charge does real work in exactly one slice (Auto Priority at peak, dose-response r = +0.80) and almost nothing on the mass tier that carries the volume; the headline +14.9% is mostly a shrinking search base, demand that recovered before the charge shipped, and an off-peak version swap. The real leak is the driver cancelling over an unpaid deadhead and the rider who gets no quote and silently leaves — neither of which is a price the meter can fix.

---

## Repo map

| Path | What's in it |
|---|---|
| [`claude.md`](claude.md) | The operating constitution: rules of engagement, writing voice, nomenclature, data-handling rules — read at the start of every session. |
| [`01_Foundation/`](01_Foundation/) | Shared problem statement of record, written before opening the data. |
| [`02_Research/`](02_Research/) | Reproducible Python (pandas) scripts, findings, and figures. Each script rebuilds every number it cites; no notebook magic. |
| [`03_Insights/verbose/`](03_Insights/verbose/) | The full answers: Part 1–5, exec summary, and narrative spine. Complete reasoning, uncut. |
| [`03_Insights/compact/`](03_Insights/compact/) | Condensed versions of each Part — the source for the PDFs sent with this submission. |
| [`04_Decision_Log/tradeoffs.md`](04_Decision_Log/tradeoffs.md) | Append-only audit trail, 19 entries: every strategic fork, the options considered, the choice, and the why. The real record of how the work was made. |
| [`pm_ai_process_onepager.html`](pm_ai_process_onepager.html) | A single-page visual anatomy of who did what across the take-home: human-led, bot-led, collaborative — and where I caught the model drifting and corrected it. |

---

## Reproduce the analysis

The raw data is not in this repo (Namma Yatri's proprietary material — see note below). With `data/rides.csv` and `data/competitor_fares.csv` in place:

```bash
pip install pandas numpy matplotlib

python3 02_Research/01_sanity_check.py          # confirms the brief's confounds are real
python3 02_Research/02_decompose_confound.py    # peak vs off-peak decomposition
python3 02_Research/04_doseresponse_placebo.py  # Test 4: dose-response + placebo
python3 02_Research/05_plots.py                 # regenerates the five figures
```

---

## A note on the data

The original brief, data dictionary, pricing experiment log, attached AI analysis, and the raw `data/*.csv` are Namma Yatri's own materials and their real (de-identified) ride data. They are intentionally excluded from this repo so it is safe to host publicly. Everything here — including the aggregated figures — is derived and presented solely for this assessment.
