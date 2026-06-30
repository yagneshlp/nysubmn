"""
09_cancellation_breakdown.py — Decompose the cancel/rides rate by actor, hour, and
distance band.

WHY THIS ANALYSIS EXISTS:
Part 1 ranked driver cancellation (H1) as the primary funnel leak, but "cancellation"
blends two structurally different behaviours. A driver who accepts then cancels is
responding to deadhead economics: the trip origin is far, the fare is short, the net
take after unpaid deadhead looks bad only after accept — because the offer card shows
the destination fare but not the pickup distance. A rider who cancels is responding to
wait time or a changed plan; that's a different root cause with a different fix.

Unless we separate driver-initiated from rider-initiated cancellations, we don't know
which lever to pull. This script checks the aggregate split, then asks whether
driver-cancel share rises at peak (where deadhead pressure is highest, short-trip
requests are densest) and on short-distance trips (where the fare rarely compensates
a long pickup). If driver-cancel spikes on short trips at peak, it validates the
deadhead hypothesis and makes the deadhead-pay experiment in Part 3 the right call.

Feeds: Part 1 (H1 decomposition), Part 3 (experiment premise), Part 4 (target hours).

Data rules: cancelled_by_driver and cancelled are additive — sum freely.
Driver-cancel share = cancelled_by_driver.sum() / cancelled.sum() within any segment.
Run: python3 02_Research/09_cancellation_breakdown.py
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
print("[A] OVERALL SPLIT — driver vs rider cancel share by tier")
print("    H1's deadhead hypothesis requires driver-initiated to dominate.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    d = R[R.service_tier == tier]
    total_cancel = d.cancelled.sum()
    driver_share = d.cancelled_by_driver.sum() / total_cancel
    rider_share = 1 - driver_share
    cancel_rate = rate(d, "cancelled", "rides")
    print(f"  {tier}:")
    print(f"     cancel/rides = {cancel_rate:.3f}   "
          f"driver-initiated = {driver_share:.0%}   rider-initiated = {rider_share:.0%}")
    print(f"     (total cancellations = {total_cancel:,.0f})")


print("\n" + "=" * 74)
print("[B] BY TIME-OF-DAY — does driver-cancel share spike at peak?")
print("    Peak = densest short-trip demand + worst deadhead economics.")
print("    A higher driver-cancel share at peak supports the deadhead mechanism.")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for tod in ["peak", "offpeak_mid", "night"]:
        d = R[(R.service_tier == tier) & (R.tod == tod)]
        if d.cancelled.sum() == 0:
            continue
        cr = rate(d, "cancelled", "rides")
        ds = d.cancelled_by_driver.sum() / d.cancelled.sum()
        print(f"     {tod:11s}: cancel/rides={cr:.3f}   driver share={ds:.0%}   "
              f"(cancellations={d.cancelled.sum():,.0f})")


print("\n" + "=" * 74)
print("[C] BY DISTANCE BAND — does driver-cancel spike on short trips?")
print("    Short trip + unknown deadhead = worst net-earnings case for a driver.")
print("    Rising driver-cancel share on short bands validates the deadhead fix.")
print("=" * 74)
dist_order = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8",
              "8-9", "9-10", "10-12", "12-16", "16+"]
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for b in dist_order:
        d = R[(R.service_tier == tier) & (R.distance_bucket == b)]
        if d.cancelled.sum() < 1000:
            continue
        cr = rate(d, "cancelled", "rides")
        ds = d.cancelled_by_driver.sum() / d.cancelled.sum()
        vol = d.rides.sum()
        print(f"     {b:6s} km: cancel/rides={cr:.3f}   driver share={ds:.0%}   "
              f"rides={vol:,.0f}")


print("\n" + "=" * 74)
print("[D] HOUR-LEVEL PROFILE — cancel rate and driver share by peak hour (Auto)")
print("    Identifies the specific hours where the deadhead problem is worst,")
print("    which informs where to target the deadhead-pay experiment first.")
print("=" * 74)
pk = R[(R.tod == "peak") & (R.service_tier == "Auto")]
print("  Auto peak hours:")
print(f"  {'hour':>4}  {'cancel/rides':>12}  {'driver share':>13}  {'comp/search':>11}  {'rides':>8}")
for h in sorted(pk.hour_bucket.unique()):
    seg = pk[pk.hour_bucket == h]
    if seg.rides.sum() == 0:
        continue
    cr = rate(seg, "cancelled", "rides")
    ds = seg.cancelled_by_driver.sum() / seg.cancelled.sum() if seg.cancelled.sum() else np.nan
    comp = rate(seg, "completed", "searches")
    rides = seg.rides.sum()
    print(f"  {h:>4}  {cr:>12.3f}  {ds:>13.0%}  {comp:>11.3f}  {rides:>8,.0f}")
