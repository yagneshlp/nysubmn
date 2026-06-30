"""
03_competitor_defection.py — Part 1 Test 5, the competitor guard, run on both ends.
Stage 1 risk: is NY priced ABOVE competitors, sending price-sensitive riders away?
Stage 3 risk: is the competitor's fare high enough that a subsidized rival can out-bid
              NY for the driver (poach), which price under zero-commission cannot answer?

Data rules honored:
- competitor_fares carries namma_yatri itself -> like-for-like benchmark.
- Compare WITHIN distance_bucket (routes skew long, ~16km median) using price_per_km_p50.
- price_per_km_p50 is a FROZEN quantile per cell: never average it across cells.
  Where a cross-cell number is needed, rebuild from fare_sum / fare_n.
- Keep Auto and Auto Priority separate. Respect serviceable_n / n (thin cells = noisy).
- PRE = up to 2026-06-09, POST = 2026-06-10 on, to read drift across the rollout.
Run: python3 02_Research/03_competitor_defection.py
"""
import pandas as pd, numpy as np

C = pd.read_csv("data/competitor_fares.csv",
                dtype={"hour_bucket": str, "distance_bucket": str})
for col in ["fare_p25","fare_p50","fare_p75","list_fare_p50","fare_sum",
            "price_per_km_p50","eta_min_p50"]:
    C[col] = pd.to_numeric(C[col], errors="coerce")
C["period"] = np.where(C.date <= "2026-06-09", "PRE", "POST")

# rides cube uses zero-padded hours ('08') + '16+'; competitor uses '8' + '16-48'.
# Normalize so the two could be joined later; here we stay inside competitor_fares.
peak = {"8", "9", "10", "16", "17", "18", "19", "20"}
C["tod"] = np.where(C.hour_bucket.isin(peak), "peak", "offpeak_mid")

def ppk_rebuilt(df):
    """cross-cell price/km via additive fare_sum / fare_n (NOT a median of medians)."""
    fn = df["fare_n"].sum()
    return df["fare_sum"].sum() / fn if fn else np.nan

print("=" * 74)
print("[A] Coverage — what overlaps with NY at all (Auto, by distance band)")
print("=" * 74)
comps = ["namma_yatri", "competitor1", "competitor2"]
auto = C[C.vehicle == "Auto"]
for v in comps:
    d = auto[auto.competitor == v]
    print(f"  {v:13s}: rows={len(d):5d}  serviceable_n_sum={d.serviceable_n.sum():>8,}  "
          f"dist_bands={d.distance_bucket.nunique()}")

print("\n" + "=" * 74)
print("[B] STAGE-1 GUARD — NY price_per_km vs rivals, WITHIN distance band (Auto)")
print("    positive gap = NY more expensive per km = rider-defection pressure")
print("=" * 74)
dist_order = ["1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16-48"]
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --   (PRE -> POST NY ppk gap vs cheapest rival, per band)")
    T = C[C.vehicle == tier]
    for period in ["PRE", "POST"]:
        P = T[T.period == period]
        ny = P[P.competitor == "namma_yatri"]
        riv = P[P.competitor != "namma_yatri"]
        line = []
        for b in dist_order:
            nyb = ny[ny.distance_bucket == b]
            rvb = riv[riv.distance_bucket == b]
            if nyb.serviceable_n.sum() < 20 or rvb.serviceable_n.sum() < 20:
                continue
            ny_ppk = ppk_rebuilt(nyb)
            rv_ppk = ppk_rebuilt(rvb)
            gap = (ny_ppk / rv_ppk - 1) * 100
            line.append(f"{b}:{gap:+.0f}%")
        print(f"     {period:4s}: " + "  ".join(line))

print("\n" + "=" * 74)
print("[C] DRIFT — did NY get relatively MORE expensive across the rollout? (Auto)")
print("    blended NY-vs-rival ppk gap, rebuilt additive, peak vs offpeak")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    print(f"  -- {tier} --")
    for tod in ["peak", "offpeak_mid"]:
        row = []
        for period in ["PRE", "POST"]:
            seg = C[(C.vehicle == tier) & (C.tod == tod) & (C.period == period)]
            ny = ppk_rebuilt(seg[seg.competitor == "namma_yatri"])
            rv = ppk_rebuilt(seg[seg.competitor != "namma_yatri"])
            gap = (ny / rv - 1) * 100 if ny and rv else np.nan
            row.append(f"{period}={gap:+.1f}%")
        print(f"     {tod:11s}: " + "  ".join(row))

print("\n" + "=" * 74)
print("[D] ETA gap — is NY slower? (rider's other reason to walk at Stage 1)")
print("    eta_min_p50 is a frozen quantile: report band-level, do not average")
print("=" * 74)
for tier in ["Auto", "Auto Priority"]:
    P = C[(C.vehicle == tier) & (C.period == "POST")]
    bands = ["2-3", "4-5", "6-7", "9-10", "12-16"]
    print(f"  -- {tier} (POST, eta_min_p50 by band) --")
    for b in bands:
        vals = []
        for v in comps:
            cell = P[(P.competitor == v) & (P.distance_bucket == b)]
            if cell.serviceable_n.sum() >= 20 and len(cell):
                # single representative cell median weighted pick: take the max-n cell's p50
                top = cell.sort_values("serviceable_n").iloc[-1]
                vals.append(f"{v.split('_')[0][:4]}={top.eta_min_p50:.0f}")
        if vals:
            print(f"     {b:6s}: " + "  ".join(vals))
