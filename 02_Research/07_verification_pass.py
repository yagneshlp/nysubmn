"""
07_verification_pass.py — Director-review verification pass (Step 1).
Three questions raised in review, all answerable in the cube:

  Q1  THIN-CELL CHECK on Finding 1 (the one staked positive). Show n on every
      AP 250-vs-252 peak band. Does r=+0.80 survive when we weight/trim by sample?
  Q2  WHY DID AUTO SEARCHES FALL 181k->168k? Seasonality (uniform across hours),
      retry collapse, or a real demand exit? Decompose the denominator.
  Q3  NAME THE SYSTEM-WIDE CAUSE behind the placebo lift. Do the acceptance-first
      versions (211/245/247/248) or a supply/cancellation shift track the
      night/off-peak completion jump that pricing cannot explain?

Conventions match 04_doseresponse_placebo.py: applied surge REBUILT from
congestion_sum/congestion_n, completion = completed/searches, raw count tracked,
Auto and Auto Priority never blended.
Run: python3 02_Research/07_verification_pass.py
"""
import pandas as pd, numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08","09","10","16","17","18","19","20"}
R["tod"] = R.hour_bucket.map(lambda h: "night" if h == "night(23-06)"
                             else ("peak" if h in peak else "offpeak_mid"))
def rate(d,n,de): return d[n].sum()/d[de].sum() if d[de].sum() else np.nan
def cong(d):      return d.congestion_sum.sum()/d.congestion_n.sum() if d.congestion_n.sum() else np.nan
dist_order = ["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16+"]

print("="*82)
print("[Q1] THIN-CELL CHECK — Finding 1: AP 250-vs-252 in PEAK, n shown on every band")
print("     weighted corr + leave-thin-bands-out test; does the staked +0.80 hold?")
print("="*82)
pk = R[(R.tod=="peak") & (R.pricing_version.isin(["250","252"]))]
T = pk[pk.service_tier=="Auto Priority"]
rows=[]
for b in dist_order:
    d250=T[(T.pricing_version=="250")&(T.distance_bucket==b)]
    d252=T[(T.pricing_version=="252")&(T.distance_bucket==b)]
    n250, n252 = d250.searches.sum(), d252.searches.sum()
    nmin=min(n250,n252)
    if nmin<=0: continue
    dc = cong(d252)-cong(d250)
    dcomp = rate(d252,"completed","searches")-rate(d250,"completed","searches")
    rows.append((b,dc,dcomp,nmin,n250,n252))
    flag = "  <-- THIN" if nmin<300 else ""
    print(f"   {b:6s}: Dcong={dc:+.3f}  Dcomp={dcomp:+.3f}  n(250)={n250:6,.0f} n(252)={n252:6,.0f} min={nmin:6,.0f}{flag}")

dcs=np.array([r[1] for r in rows]); dcomps=np.array([r[2] for r in rows]); ns=np.array([r[3] for r in rows])
def pearson(x,y): return np.corrcoef(x,y)[0,1]
def wcorr(x,y,w):
    mx=np.average(x,weights=w); my=np.average(y,weights=w)
    cov=np.average((x-mx)*(y-my),weights=w)
    return cov/np.sqrt(np.average((x-mx)**2,weights=w)*np.average((y-my)**2,weights=w))
print(f"\n   bands total = {len(rows)}   thin (min n<300) = {sum(ns<300)}")
print(f"   unweighted corr(Dcong,Dcomp)           = {pearson(dcs,dcomps):+.2f}  (this is the staked +0.80)")
print(f"   search-weighted corr                   = {wcorr(dcs,dcomps,ns):+.2f}")
m=ns>=300
if m.sum()>=3:
    print(f"   corr on dense bands only (n>=300, {m.sum()} bands) = {pearson(dcs[m],dcomps[m]):+.2f}")
print(f"   share of AP-peak searches in dense bands = {ns[m].sum()/ns.sum():.0%}")

print("\n"+"="*82)
print("[Q2] WHY DID AUTO SEARCHES FALL 181k->168k? decompose the denominator")
print("="*82)
A=R[R.service_tier=="Auto"]
for lbl,lo,hi,days in [("Jun01-09",'2026-06-01','2026-06-09',9),("Jun10-22",'2026-06-10','2026-06-22',13)]:
    w=A[(A.date>=lo)&(A.date<=hi)]
    print(f"  {lbl}: searches/day={w.searches.sum()/days:8,.0f}  retries/day={w.retries.sum()/days:8,.0f}  "
          f"completed/day={w.completed.sum()/days:8,.0f}  ret/search={w.retries.sum()/w.searches.sum():.3f}")
print("  -- searches/day by time-of-day (is the drop uniform=seasonal, or concentrated?) --")
for tod in ["peak","offpeak_mid","night"]:
    a=A[(A.tod==tod)&(A.date>='2026-06-01')&(A.date<='2026-06-09')]
    z=A[(A.tod==tod)&(A.date>='2026-06-10')&(A.date<='2026-06-22')]
    sa,sz=a.searches.sum()/9, z.searches.sum()/13
    print(f"     {tod:11s}: {sa:8,.0f} -> {sz:8,.0f}  ({(sz/sa-1)*100:+5.1f}%)")
print("  -- weekday-only (strip weekend mix) Auto searches/day --")
for lbl,lo,hi,days in [("Jun01-09",'2026-06-01','2026-06-09',9),("Jun10-22",'2026-06-10','2026-06-22',13)]:
    w=A[(A.date>=lo)&(A.date<=hi)&(A.is_weekend==0)]
    wd=len(w.date.unique())
    print(f"     {lbl} weekdays={wd}: searches/weekday={w.searches.sum()/wd:8,.0f}")

print("\n"+"="*82)
print("[Q3] NAME THE SYSTEM-WIDE CAUSE — what moved completion where surge didn't?")
print("="*82)
print("  -- (a) version MIX shift PRE->POST in night+offpeak Auto (the placebo zone) --")
plc=A[A.tod.isin(["night","offpeak_mid"])]
for lbl,lo,hi in [("PRE  May18-Jun09",'2026-05-18','2026-06-09'),("POST Jun10-22",'2026-06-10','2026-06-22')]:
    w=plc[(plc.date>=lo)&(plc.date<=hi)]
    tot=w.searches.sum()
    mix=w.groupby("pricing_version").searches.sum().sort_values(ascending=False)
    top=" ".join(f"v{v}:{s/tot:.0%}" for v,s in mix.head(5).items())
    print(f"     {lbl}: {top}")
print("  -- (b) completion by version in the placebo zone (acceptance-first vs congestion) --")
af={"211","245","247","248"}; cg={"234","236","240","250","252"}
for fam,vers in [("acceptance-first",af),("congestion-up",cg)]:
    w=plc[plc.pricing_version.isin(vers)]
    if w.searches.sum()>0:
        print(f"     {fam:16s}: comp/search={rate(w,'completed','searches'):.3f}  cong={cong(w):.2f}  "
              f"searches={w.searches.sum():,.0f}")
print("  -- (c) cancellation + supply proxies PRE->POST in placebo zone (system-wide?) --")
for lbl,lo,hi in [("PRE ",'2026-05-18','2026-06-09'),("POST",'2026-06-10','2026-06-22')]:
    w=plc[(plc.date>=lo)&(plc.date<=hi)]
    cr=w.cancelled.sum()/w.rides.sum(); dshare=w.cancelled_by_driver.sum()/w.cancelled.sum()
    acc=w.rider_acceptances.sum()/w.searches.sum(); r2r=w.completed.sum()/w.rides.sum()
    print(f"     {lbl}: cancel/ride={cr:.3f}  drvshare={dshare:.3f}  acc/search={acc:.3f}  completed/ride={r2r:.3f}")
print("  -- (d) same split, PEAK Auto, to see if the move is system-wide or peak-only --")
pkA=A[A.tod=="peak"]
for lbl,lo,hi in [("PRE ",'2026-05-18','2026-06-09'),("POST",'2026-06-10','2026-06-22')]:
    w=pkA[(pkA.date>=lo)&(pkA.date<=hi)]
    cr=w.cancelled.sum()/w.rides.sum(); acc=w.rider_acceptances.sum()/w.searches.sum(); r2r=w.completed.sum()/w.rides.sum()
    print(f"     {lbl}: cancel/ride={cr:.3f}  acc/search={acc:.3f}  completed/ride={r2r:.3f}  comp/search={rate(w,'completed','searches'):.3f}")
