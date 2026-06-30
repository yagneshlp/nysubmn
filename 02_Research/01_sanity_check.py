"""
01_sanity_check.py — Ground the Part 1 framing in the actual data.
Goal: confirm (or kill) the confounds the brief warns about, BEFORE we frame hypotheses.
Rules honored: only sum additive cols; never average a p* quantile across cells.
Run: python3 02_Research/01_sanity_check.py
"""
import pandas as pd, numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version":str, "hour_bucket":str})

def rate(df, num, den):
    return df[num].sum() / df[den].sum() if df[den].sum() else np.nan

# --- Peak / off-peak buckets per brief: peak ~08-11 and 16-20 ---
peak = {"08","09","10","16","17","18","19","20"}
def tod(h):
    if h == "night(23-06)": return "night"
    return "peak" if h in peak else "offpeak_mid"
R["tod"] = R["hour_bucket"].map(tod)

print("="*70)
print("[A] REPLICATE THE AI ANALYSIS: naive all-auto before/after on completion/search")
print("="*70)
pre  = R[(R.date <= "2026-06-09")]
post = R[(R.date >= "2026-06-10")]
for lbl, d in [("PRE (May18-Jun9)", pre), ("POST(Jun10-Jun22)", post)]:
    print(f"  {lbl}: completion/search = {rate(d,'completed','searches'):.3f}  "
          f"avg_fare = {d['completed_fare_sum'].sum()/d['completed'].sum():.1f}  "
          f"cancel/rides = {rate(d,'cancelled','rides'):.3f}")
lift = rate(post,'completed','searches')/rate(pre,'completed','searches') - 1
print(f"  -> naive lift in completion/search = {lift*100:+.1f}%   (AI claimed +14.9%)")

print("\n"+"="*70)
print("[B] CONFOUND #1 — is version assignment gated by time-of-day?")
print("    share of each version's SEARCHES by time-of-day bucket")
print("="*70)
for v in ["211","234","236","250","252"]:
    d = R[R.pricing_version==v]
    tot = d["searches"].sum()
    row = {t: d[d.tod==t]["searches"].sum()/tot for t in ["peak","offpeak_mid","night"]}
    print(f"  v{v}: peak={row['peak']:.0%}  offpeak/mid={row['offpeak_mid']:.0%}  night={row['night']:.0%}  (searches={tot:,})")

print("\n  Evening-peak (16-20) version mix — does 236 vanish here?")
ev = R[R.hour_bucket.isin(["16","17","18","19","20"])]
mix = ev.groupby("pricing_version")["searches"].sum().sort_values(ascending=False)
for v,s in mix.items(): print(f"     v{v}: {s/mix.sum():.0%}")

print("\n"+"="*70)
print("[C] CONFOUND CHECK — is DISTANCE confounded? (brief says NO)")
print("    share of searches by distance band, per version")
print("="*70)
dist_order = ["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16+"]
for v in ["236","250","252"]:
    d = R[R.pricing_version==v]; tot=d["searches"].sum()
    sh = [d[d.distance_bucket==b]["searches"].sum()/tot for b in dist_order]
    print(f"  v{v}: " + " ".join(f"{b}:{x:.0%}" for b,x in zip(dist_order,sh) if x>0.02))

print("\n"+"="*70)
print("[D] THE CLEAN COMPARISON — 250 vs 252 INSIDE PEAK, split by tier")
print("="*70)
pk = R[(R.tod=="peak") & (R.pricing_version.isin(["250","252"]))]
for tier in ["Auto","Auto Priority"]:
    print(f"  -- {tier} --")
    for v in ["250","252"]:
        d = pk[(pk.service_tier==tier) & (pk.pricing_version==v)]
        if d["searches"].sum()==0: continue
        avg_cong = d["congestion_sum"].sum()/d["congestion_n"].sum()
        print(f"     v{v}: comp/search={rate(d,'completed','searches'):.3f}  "
              f"cancel/rides={rate(d,'cancelled','rides'):.3f}  "
              f"drv-cancel-share={rate(d,'cancelled_by_driver','cancelled'):.2f}  "
              f"avg_cong={avg_cong:.3f}  avg_fare={d['completed_fare_sum'].sum()/d['completed'].sum():.0f}  "
              f"searches={d['searches'].sum():,}")

print("\n"+"="*70)
print("[E] DAILY COMPLETED RIDES — did they 'slip in May, tick up after Jun10'?")
print("    (Auto vs Auto Priority separately)")
print("="*70)
for tier in ["Auto","Auto Priority"]:
    d = R[R.service_tier==tier].groupby("date")["completed"].sum()
    wk = d.groupby(pd.to_datetime(d.index).isocalendar().week.values).sum()
    print(f"  {tier}: completed/day  "
          f"May18-24~{d['2026-05-18':'2026-05-24'].mean():.0f}  "
          f"May25-31~{d['2026-05-25':'2026-05-31'].mean():.0f}  "
          f"Jun01-09~{d['2026-06-01':'2026-06-09'].mean():.0f}  "
          f"Jun10-22~{d['2026-06-10':'2026-06-22'].mean():.0f}")

print("\n"+"="*70)
print("[F] FUNNEL SHAPE overall (where does the leak happen?)")
print("="*70)
for tier in ["Auto","Auto Priority"]:
    d=R[R.service_tier==tier]
    s,a,ri,c,x = (d[k].sum() for k in ["searches","rider_acceptances","rides","completed","cancelled"])
    print(f"  {tier}: searches={s:,} -> rider_acc={a:,}({a/s:.0%}) -> rides={ri:,}({ri/s:.0%}) "
          f"-> completed={c:,}({c/s:.0%}) | cancelled={x:,}(cancel/rides={x/ri:.0%})")
