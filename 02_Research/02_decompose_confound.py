"""
02_decompose_confound.py — Simpson's paradox check on the +14.9% headline lift.

WHY THIS ANALYSIS EXISTS:
The naive PRE/POST completion/search comparison (01_sanity_check.py, section A) gives
+14.9%. But v250/v252 run almost exclusively at peak hours, while the baseline v236 runs
mainly off-peak and at night. A mix-shift from off-peak toward peak would mechanically
raise the blended completion rate even if nothing changed within any single time-of-day
bucket — this is Simpson's paradox applied to version assignment.

This script holds time-of-day fixed and asks: does the lift survive when we compare like
with like? If the lift disappears inside each ToD bucket, the headline is pure composition;
if it persists, something real changed. We also check whether the search-share itself
shifted across ToD (demand mix-shift would inflate the rate even if per-bucket rates held
flat), and whether v236 actually vanished from the evening peak over time (the brief's
claim that enabled the version swap).

Section G: the main Simpson's decomposition.
Section H: demand-side mix shift — did peak's share of searches change PRE to POST?
Section I: version ramp check — did v236 really disappear from evening peak on rollout?
Section J: average congestion actually applied, additive-rebuilt, confirms the charge moved.

Data rules: pre = up to Jun 9, post = Jun 10 onward; days = 23 and 13 respectively.
Completion = completed/searches (additive numerator and denominator, safe to compare).
Congestion rebuilt from congestion_sum/congestion_n — never use the p50 quantile.
Run: python3 02_Research/02_decompose_confound.py
"""
import pandas as pd, numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08", "09", "10", "16", "17", "18", "19", "20"}
R["tod"] = R["hour_bucket"].map(
    lambda h: "night" if h == "night(23-06)" else ("peak" if h in peak else "offpeak_mid")
)

def r(d, n, de):
    return d[n].sum() / d[de].sum() if d[de].sum() else np.nan

pre = R[R.date <= "2026-06-09"]
post = R[R.date >= "2026-06-10"]

# ── [G] SIMPSON'S CHECK ────────────────────────────────────────────────────────
# If the +14.9% is a mix-shift artifact, it should evaporate when we hold ToD fixed.
# If it persists within every ToD bucket, something structural changed.
# The search-share column tells us whether the composition of demand shifted too.
print("[G] DECOMPOSE the +14.9% — completion/search PRE vs POST, holding tier & ToD fixed")
print("    If lift persists inside each bucket: real. If it vanishes: mix-shift artifact.")
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for t in ["peak", "offpeak_mid", "night"]:
        a = pre[(pre.service_tier == tier) & (pre.tod == t)]
        b = post[(post.service_tier == tier) & (post.tod == t)]
        if a["searches"].sum() == 0 or b["searches"].sum() == 0:
            continue
        pre_r = r(a, "completed", "searches")
        post_r = r(b, "completed", "searches")
        lift = (post_r / pre_r - 1) * 100 if pre_r else np.nan
        # search-share tells us if peak's share of total demand shifted (another confound layer)
        pre_share = a["searches"].sum() / pre[pre.service_tier == tier]["searches"].sum()
        post_share = b["searches"].sum() / post[post.service_tier == tier]["searches"].sum()
        print(f"     {t:12s}: PRE {pre_r:.3f} -> POST {post_r:.3f}  ({lift:+.1f}%)  "
              f"search-share PRE {pre_share:.0%} -> POST {post_share:.0%}")

# ── [H] DEMAND MIX SHIFT ────────────────────────────────────────────────────────
# Even if per-bucket rates are unchanged, a shift in WHICH bucket carries more searches
# can move the blended rate. Check whether peak's share of total Auto searches grew.
print("\n[H] Demand mix shift — total searches PRE vs POST by ToD (Auto only)")
print("    A stable search-share means the +14.9% is not a reweighting artifact.")
A = R[R.service_tier == "Auto"]
for t in ["peak", "offpeak_mid", "night"]:
    pa = A[(A.date <= "2026-06-09") & (A.tod == t)]["searches"].sum()
    po = A[(A.date >= "2026-06-10") & (A.tod == t)]["searches"].sum()
    # normalize per day — pre=23 days, post=13 days — to make volumes comparable
    print(f"   {t:12s}: PRE {pa/23:,.0f}/day   POST {po/13:,.0f}/day   ({(po/13)/(pa/23)-1:+.0%})")

# ── [I] VERSION RAMP — did v236 actually leave evening peak? ──────────────────
# The brief asserts v236 was phased out of evening peak during rollout. If true,
# the switch from a lower-clearing version to v250/v252 explains some of the
# off-peak/night lift (the placebo) via a matching-algorithm improvement, not pricing.
print("\n[I] Does v236 actually vanish in evening peak (16-20)? share over time (Auto)")
ev = R[(R.hour_bucket.isin(["16", "17", "18", "19", "20"])) & (R.service_tier == "Auto")]
for win, lo, hi in [("May18-31", "2026-05-18", "2026-05-31"),
                     ("Jun01-09", "2026-06-01", "2026-06-09"),
                     ("Jun10-22", "2026-06-10", "2026-06-22")]:
    d = ev[(ev.date >= lo) & (ev.date <= hi)]
    tot = d["searches"].sum()
    sh = d.groupby("pricing_version")["searches"].sum().sort_values(ascending=False) / tot
    top = " ".join(f"v{v}:{x:.0%}" for v, x in sh.head(5).items())
    print(f"   {win}: {top}")

# ── [J] CONGESTION ACTUALLY APPLIED ────────────────────────────────────────────
# Confirms the charge really moved (otherwise there's nothing to attribute the lift to).
# MUST be rebuilt from congestion_sum/congestion_n — never average the p50 across cells.
print("\n[J] Weighted avg congestion actually applied, by tier & period (additive-built)")
print("    Rebuilt from sum/n, not averaged from p50 — the only valid cross-cell read.")
for tier in ["Auto", "Auto Priority"]:
    for lbl, d in [("PRE", pre), ("POST", post)]:
        dd = d[d.service_tier == tier]
        avg_cong = dd["congestion_sum"].sum() / dd["congestion_n"].sum()
        avg_fare = dd["completed_fare_sum"].sum() / dd["completed"].sum()
        print(f"   {tier:14s} {lbl}: avg_cong={avg_cong:.3f}  avg_fare=₹{avg_fare:.1f}")
