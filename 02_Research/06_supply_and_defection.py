"""
06_supply_and_defection.py — evidence for Part 4 (defended lever = supply-shaping).
(1) Is demand PREDICTABLE enough to shape supply against it? (regularity of searches by hour)
(2) Where does the completion loop actually leak by hour? (target for repositioning)
(3) Competitor defection HEADROOM: how far below rivals is NY, i.e. how much room before a
    higher congestion charge would price riders above the market. Rebuilt additive within band.
Run: python3 02_Research/06_supply_and_defection.py
"""
import pandas as pd, numpy as np
R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
C = pd.read_csv("data/competitor_fares.csv", dtype={"hour_bucket": str, "distance_bucket": str})
for c in ["fare_sum"]: C[c] = pd.to_numeric(C[c], errors="coerce")

def rate(d,n,de): return d[n].sum()/d[de].sum() if d[de].sum() else np.nan

print("="*72)
print("[1] IS DEMAND PREDICTABLE? day-to-day stability of the searches-by-hour shape")
print("    (low coefficient of variation across dates = a shapeable, recurring pattern)")
print("="*72)
A = R[R.service_tier=="Auto"]
# searches per (date, hour); then CV across dates within each hour, weekday only
wd = A[A.is_weekend==0]
piv = wd.groupby(["date","hour_bucket"])["searches"].sum().reset_index()
cv = piv.groupby("hour_bucket")["searches"].agg(["mean","std"])
cv["cv"] = cv["std"]/cv["mean"]
print("  weekday searches/hour: mean, and coefficient of variation across the 25 weekdays")
for h,row in cv.iterrows():
    bar = "#"*int(row["mean"]/ piv["searches"].max()*40)
    print(f"   {h:>12}: mean={row['mean']:8,.0f}  CV={row['cv']:.2f}  {bar}")
print(f"  --> median hourly CV = {cv['cv'].median():.2f}  (｢<0.25｣ = highly regular/predictable)")

print("\n"+"="*72)
print("[2] WHERE DOES THE LOOP LEAK BY HOUR? completion/search by hour (Auto)  ")
print("    low-completion hours = where shaping supply onto unmet demand pays off")
print("="*72)
by_h = A.groupby("hour_bucket").apply(lambda d: pd.Series({
    "searches/day": d["searches"].sum()/ d["date"].nunique(),
    "comp/search": rate(d,"completed","searches"),
    "cancel/rides": rate(d,"cancelled","rides")}), include_groups=False)
print(by_h.round(3).to_string())

print("\n"+"="*72)
print("[3] DEFECTION HEADROOM — clean WITHIN-BAND read (peak). gap<0 = NY cheaper.")
print("    NOTE: pooled peak gap looks ~-2%/-6%, but that is DISTANCE-CONFOUNDED")
print("    (competitor scrapes skew ~16km). Within-band is the honest headroom.")
print("="*72)
peakC = {"8","9","10","16","17","18","19","20"}
C["peak"] = C.hour_bucket.isin(peakC)
def avgfare(df):
    fn=df.fare_n.sum(); return df.fare_sum.sum()/fn if fn else np.nan
bands = ["1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16-48"]
# NY volume weights per band from rides cube (peak), to summarize honestly
Rpeak = R[R.hour_bucket.isin({"08","09","10","16","17","18","19","20"})]
for tier in ["Auto","Auto Priority"]:
    seg = C[(C.vehicle==tier) & (C.peak)]
    wtot, gsum, line = 0.0, 0.0, []
    rb = "16+" if False else None
    for b in bands:
        nyb = seg[(seg.competitor=="namma_yatri") & (seg.distance_bucket==b)]
        rvb = seg[(seg.competitor!="namma_yatri") & (seg.distance_bucket==b)]
        if nyb.serviceable_n.sum()<20 or rvb.serviceable_n.sum()<20: continue
        ny = avgfare(nyb); cheaper = min(avgfare(rvb[rvb.competitor=="competitor1"]),
                                         avgfare(rvb[rvb.competitor=="competitor2"]))
        gap = ny/cheaper - 1
        # weight by NY peak ride volume in matching rides-cube band
        rbk = "16+" if b=="16-48" else b
        w = Rpeak[(Rpeak.service_tier==tier)&(Rpeak.distance_bucket==rbk)]["completed"].sum()
        wtot += w; gsum += w*gap
        line.append(f"{b}:{gap:+.0%}")
    wavg = gsum/wtot if wtot else np.nan
    print(f"  {tier}:")
    print(f"     by band: " + "  ".join(line))
    print(f"     NY-volume-weighted headroom below cheapest rival = {wavg:+.0%}  "
          f"(room before a higher charge crosses the market)")
