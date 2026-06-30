"""
10_weekly_trend.py — Week-by-week completion trend to distinguish structural shift from
mean reversion or seasonal recovery.

WHY THIS ANALYSIS EXISTS:
The PRE/POST comparison in 01_sanity_check.py is a snapshot: average before vs average
after. It cannot tell us whether the improvement happened at the rollout date (a step-
change consistent with a causal effect) or whether rides were already recovering on a
gradual upward trend before v250/v252 appeared (mean reversion or seasonal recovery, which
would inflate any before-after estimate).

A genuine pricing effect should show a visible step-change at or near Jun 10 (the rollout
date). A recovery trend would show a smooth week-on-week rise that passes through the
rollout date without a visible kink. The difference matters: if it's a step-change,
Part 2's finding that the pricing did real work on Auto Priority peak is more credible;
if it's a smooth recovery, the congestion charge is riding a trend it didn't create.

This script also separates weekday from weekend to check whether the effect is concentrated
in commuter hours (where pricing fires) or distributed across all trip types. A pricing
effect should be stronger on weekdays where peak congestion is worst.

Feeds: Part 2 (Finding 2, the +14.9% diagnosis), Part 5 (honest gap: no exogenous
controls means we can't fully rule out seasonal recovery).

Data rules: all additive. Completion = completed/searches.
Run: python3 02_Research/10_weekly_trend.py
"""

import pandas as pd
import numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
R["date_dt"] = pd.to_datetime(R["date"])
R["iso_week"] = R["date_dt"].dt.isocalendar().week.astype(int)

def rate(d, n, de):
    return d[n].sum() / d[de].sum() if d[de].sum() else np.nan


print("=" * 74)
print("[A] WEEK-ON-WEEK COMPLETION RATE — step-change at rollout or smooth recovery?")
print("    Jun 10 (week 24) is the rollout date. A genuine pricing effect should show")
print("    a visible kink there; a recovery trend should be smooth through it.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    d = R[R.service_tier == tier]
    for wk in sorted(d.iso_week.unique()):
        w = d[d.iso_week == wk]
        dates = sorted(w.date.unique())
        date_range = f"{dates[0]} to {dates[-1]}"
        comp = rate(w, "completed", "searches")
        searches_day = w.searches.sum() / len(dates)
        cancel = rate(w, "cancelled", "rides")
        marker = "  <-- ROLLOUT" if wk == 24 else ""
        print(f"     week {wk} ({date_range}): "
              f"comp/search={comp:.3f}   searches/day={searches_day:,.0f}   "
              f"cancel/rides={cancel:.3f}{marker}")


print("\n" + "=" * 74)
print("[B] WEEKDAY vs WEEKEND — is the lift concentrated in commuter hours?")
print("    If the improvement is pricing-driven, it should be stronger on weekdays")
print("    (where AM/PM peak congestion fires) than on weekends.")
print("=" * 74)
pre = R[R.date <= "2026-06-09"]
post = R[R.date >= "2026-06-10"]
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for is_wkend, label in [(0, "Weekday"), (1, "Weekend")]:
        a = pre[(pre.service_tier == tier) & (pre.is_weekend == is_wkend)]
        z = post[(post.service_tier == tier) & (post.is_weekend == is_wkend)]
        if a.searches.sum() == 0:
            continue
        pre_r = rate(a, "completed", "searches")
        post_r = rate(z, "completed", "searches")
        lift = (post_r / pre_r - 1) * 100 if pre_r else np.nan
        print(f"     {label}: PRE={pre_r:.3f}  POST={post_r:.3f}  lift={lift:+.1f}%   "
              f"(pre searches={a.searches.sum():,.0f}, post={z.searches.sum():,.0f})")


print("\n" + "=" * 74)
print("[C] DAILY COMPLETION RATE — raw time series to read the shape of the trend")
print("    Looking for: step-change at Jun 10, pre-trend already rising, or")
print("    post-trend flattening (one-off effect rather than structural shift).")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    d = R[R.service_tier == tier]
    daily = (
        d.groupby("date")
        .apply(lambda x: pd.Series({
            "comp_search": rate(x, "completed", "searches"),
            "searches": x.searches.sum(),
            "completed": x.completed.sum(),
        }), include_groups=False)
        .sort_index()
    )
    print(f"\n  {tier} — daily comp/search:")
    for dt, row in daily.iterrows():
        marker = " <-- rollout" if dt == "2026-06-10" else ""
        bar = "▓" * int(row["comp_search"] * 60)
        print(f"     {dt}: {row['comp_search']:.3f}  {bar}{marker}")
