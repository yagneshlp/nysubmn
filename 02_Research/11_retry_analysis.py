"""
11_retry_analysis.py — Analyse retry behaviour and the acc/search inflation problem.

WHY THIS ANALYSIS EXISTS:
During data validation, we found rider_acceptances (Auto: ~9.5M) exceeds searches
(Auto: ~6.36M). This means acc/search > 1 — which is impossible if you treat it as
a conversion rate. The explanation is retries: a rider who searches, fails to get a
match or gets an expensive quote, and then searches again within the same journey
generates multiple search events and potentially multiple acceptance events. The cube
aggregates these at the date × hour × tier × version × distance grain, so there is
no way to collapse them to unique journeys.

This matters for two reasons:
  1. Anyone computing acc/search as "the share of searches that get a rider
     acceptance" gets a number above 1.0, which makes the funnel arithmetic wrong.
     The valid conversion metric anchored on searches is completed/searches.
  2. Retry volume is a proxy for unmet demand — the invisible pool of riders who
     searched, got nothing useful, and tried again before giving up or switching apps.
     Part 5 identifies this as one of the structural gaps the data cannot close
     without instrumenting the search event with a reason code and a quoted fare.

This script quantifies the retry volume, checks whether retries concentrate at peak
(where match failure is most likely), and reads the PRE vs POST shift in retry rate
to ask whether the pricing change affected the frequency of failed searches.

Data rules: retries is additive — sum freely. Do not construct per-rider retention
from it; there are no rider IDs.
Run: python3 02_Research/11_retry_analysis.py
"""

import pandas as pd
import numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08", "09", "10", "16", "17", "18", "19", "20"}
R["tod"] = R.hour_bucket.map(
    lambda h: "night" if h == "night(23-06)"
    else ("peak" if h in peak else "offpeak_mid")
)

def rate(d, n, de):
    return d[n].sum() / d[de].sum() if d[de].sum() else np.nan


print("=" * 74)
print("[A] THE acc/search > 1 PROBLEM — confirm the inflation by tier")
print("    acc/search > 1 flags that acceptances per search is an amplification,")
print("    not a conversion rate. completed/searches is the valid funnel metric.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    d = R[R.service_tier == tier]
    searches = d.searches.sum()
    acc = d.rider_acceptances.sum()
    retries = d.retries.sum()
    completed = d.completed.sum()
    print(f"  {tier}:")
    print(f"     searches={searches:,.0f}   rider_acceptances={acc:,.0f}   "
          f"acc/search={acc/searches:.2f}  (not a valid conversion rate — exceeds 1)")
    print(f"     retries={retries:,.0f}   retry/search={retries/searches:.2f}")
    print(f"     completed={completed:,.0f}   completed/searches={completed/searches:.3f}  (valid)")


print("\n" + "=" * 74)
print("[B] RETRY RATE BY TIME-OF-DAY — do retries concentrate at peak?")
print("    If retry/search is highest at peak, that is a signal of match failure:")
print("    riders searching, not getting a usable quote, trying again.")
print("    This is the invisible demand Part 5 names as structurally unobservable.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for tod in ["peak", "offpeak_mid", "night"]:
        d = R[(R.service_tier == tier) & (R.tod == tod)]
        if d.searches.sum() == 0:
            continue
        rps = d.retries.sum() / d.searches.sum()
        comp = rate(d, "completed", "searches")
        print(f"     {tod:11s}: retry/search={rps:.3f}   comp/search={comp:.3f}   "
              f"(searches={d.searches.sum():,.0f})")


print("\n" + "=" * 74)
print("[C] RETRY RATE PRE vs POST — did the pricing change retry behaviour?")
print("    A drop in retry rate post-rollout would suggest fewer failed matches.")
print("    A rise would suggest fare quotes are triggering re-search (price rejection).")
print("=" * 74)
pre = R[R.date <= "2026-06-09"]
post = R[R.date >= "2026-06-10"]
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for lbl, d in [("PRE  (May18–Jun9)", pre), ("POST (Jun10–22)", post)]:
        seg = d[d.service_tier == tier]
        if seg.searches.sum() == 0:
            continue
        rps = seg.retries.sum() / seg.searches.sum()
        comp = rate(seg, "completed", "searches")
        cancel = rate(seg, "cancelled", "rides")
        print(f"     {lbl}: retry/search={rps:.3f}   comp/search={comp:.3f}   "
              f"cancel/rides={cancel:.3f}   (searches={seg.searches.sum():,.0f})")


print("\n" + "=" * 74)
print("[D] RETRY RATE BY DISTANCE BAND — where do most retries happen?")
print("    Short trips with no available drivers generate the most retries;")
print("    long trips are underserved differently (driver reluctance, not supply absence).")
print("=" * 74)
dist_order = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
              "8-9", "9-10", "10-12", "12-16", "16+"]
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for b in dist_order:
        d = R[(R.service_tier == tier) & (R.distance_bucket == b)]
        if d.searches.sum() < 10000:
            continue
        rps = d.retries.sum() / d.searches.sum()
        comp = rate(d, "completed", "searches")
        print(f"     {b:6s} km: retry/search={rps:.3f}   comp/search={comp:.3f}   "
              f"(searches={d.searches.sum():,.0f})")
