"""
12_peak_supply_gap.py — Identify the specific hours where supply-shaping yields the
highest return: high demand volume paired with low completion rate.

WHY THIS ANALYSIS EXISTS:
Part 4's defended lever is supply-shaping — using NY's own ride history to forecast
where demand will appear and nudging drivers to pre-position before the peak fires.
But "position drivers at peak" is not a product decision; it is a direction. The
actionable version requires naming the exact target windows: which hours have the
highest search volume AND the lowest completion rate, meaning demand is present but
supply is structurally absent.

This script cross-plots searches/day (demand) against completion/search (supply
meeting demand) by hour, and computes a gap score = searches/day × (1 − comp/search).
A high gap score means a lot of demand is not converting — this is exactly where a
driver who goes online would find and complete a ride rather than wait in a queue.

The stability check (section B) confirms whether the hourly demand pattern is
consistent enough across weekdays to be forecastable. If the CV at a given hour is
below 0.25, tomorrow's demand at that hour is predictable from history — which is
the prerequisite for a go-online nudge to be actionable rather than speculative.

Feeds directly into Part 4's supply-shaping section and the specific window named
for the go-online nudge lever (the evening peak window where gap score is highest).

Data rules: all additive sums. Completion = completed/searches.
Run: python3 02_Research/12_peak_supply_gap.py
"""

import pandas as pd
import numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
R["date_dt"] = pd.to_datetime(R["date"])

def rate(d, n, de):
    return d[n].sum() / d[de].sum() if d[de].sum() else np.nan


print("=" * 74)
print("[A] HOURLY COMPLETION PROFILE — high demand, low completion = supply gap")
print("    Weekday-only to strip weekend mix. Hours where searches are high")
print("    but comp/search is low are the exact target for supply pre-positioning.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} (weekday only) --")
    d = R[(R.service_tier == tier) & (R.is_weekend == 0)]
    n_days = d.date.nunique()
    # exclude the aggregated night bucket for cleaner hour-level read
    hours = sorted(h for h in d.hour_bucket.unique() if h != "night(23-06)")
    rows = []
    for h in hours:
        seg = d[d.hour_bucket == h]
        searches_day = seg.searches.sum() / n_days
        comp = rate(seg, "completed", "searches")
        cancel = rate(seg, "cancelled", "rides")
        rows.append((h, searches_day, comp, cancel))
    # sort by demand volume so the high-opportunity hours stand out
    rows.sort(key=lambda x: -x[1])
    print(f"  {'hour':>4}  {'searches/day':>13}  {'comp/search':>11}  {'cancel/rides':>12}  note")
    for h, s, c, cn in rows:
        flag = "  ← HIGH DEMAND + LOW COMPLETION" if s > 4000 and (c is None or c < 0.50) else ""
        c_str = f"{c:.3f}" if c is not None else "  n/a"
        cn_str = f"{cn:.3f}" if cn is not None else "  n/a"
        print(f"  {h:>4}  {s:>13,.0f}  {c_str:>11}  {cn_str:>12}{flag}")


print("\n" + "=" * 74)
print("[B] DEMAND STABILITY — is the hourly pattern regular enough to forecast?")
print("    Coefficient of variation (CV) across weekdays within each hour.")
print("    CV < 0.25: highly predictable → supply-shaping is actionable here.")
print("    CV > 0.40: too variable → pre-positioning would often misfire.")
print("=" * 74)
A_wd = R[(R.service_tier == "Auto") & (R.is_weekend == 0)]
piv = A_wd.groupby(["date", "hour_bucket"])["searches"].sum().reset_index()
stats = piv.groupby("hour_bucket")["searches"].agg(["mean", "std"])
stats["cv"] = stats["std"] / stats["mean"]
stats = stats[stats.index != "night(23-06)"].sort_values("mean", ascending=False)
print(f"  {'hour':>12}  {'mean searches/day':>18}  {'CV':>6}  verdict")
for h, row in stats.iterrows():
    verdict = "shapeable" if row["cv"] < 0.25 else ("uncertain" if row["cv"] < 0.40 else "noisy")
    print(f"  {h:>12}  {row['mean']:>18,.0f}  {row['cv']:>6.2f}  {verdict}")
print(f"\n  Median hourly CV (weekday, Auto): {stats['cv'].median():.2f}")


print("\n" + "=" * 74)
print("[C] GAP SCORE — top hours by supply opportunity (demand × unmet fraction)")
print("    Gap score = searches/day × (1 − comp/search).")
print("    High score = lots of demand that isn't converting = highest supply-shaping ROI.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    d = R[(R.service_tier == tier) & (R.is_weekend == 0)]
    n_days = d.date.nunique()
    gap_rows = []
    for h in sorted(d.hour_bucket.unique()):
        if h == "night(23-06)":
            continue
        seg = d[d.hour_bucket == h]
        s = seg.searches.sum() / n_days
        c = rate(seg, "completed", "searches")
        if c is None:
            continue
        gap_score = s * (1 - c)
        gap_rows.append((h, s, c, gap_score))
    gap_rows.sort(key=lambda x: -x[3])
    print(f"\n  {tier} — top 5 hours by gap score:")
    print(f"  {'hour':>4}  {'searches/day':>13}  {'comp/search':>11}  {'gap_score':>10}")
    for h, s, c, g in gap_rows[:5]:
        print(f"  {h:>4}  {s:>13,.0f}  {c:>11.3f}  {g:>10,.0f}")
    top_hours = [r[0] for r in gap_rows[:3]]
    print(f"  → Priority window for go-online nudge: hours {', '.join(top_hours)}")


print("\n" + "=" * 74)
print("[D] EVENING PEAK DEEP DIVE — the 17–19h window in detail")
print("    Part 4's supply-shaping recommendation targets the evening peak specifically.")
print("    Check whether the gap is stable across different distance bands there,")
print("    to know whether repositioning drivers helps short trips, long trips, or both.")
print("=" * 74)
evening = R[(R.hour_bucket.isin(["17", "18", "19"])) &
            (R.service_tier == "Auto") & (R.is_weekend == 0)]
n_days = evening.date.nunique()
dist_order = ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10", "10-12"]
print(f"  Auto weekday 17–19h, by distance band:")
print(f"  {'band':>6}  {'searches/day':>13}  {'comp/search':>11}  {'cancel/rides':>12}")
for b in dist_order:
    seg = evening[evening.distance_bucket == b]
    if seg.searches.sum() < 500:
        continue
    s = seg.searches.sum() / n_days
    c = rate(seg, "completed", "searches")
    cn = rate(seg, "cancelled", "rides")
    print(f"  {b:>6}  {s:>13,.0f}  {c:>11.3f}  {cn:>12.3f}")
