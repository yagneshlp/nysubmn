"""
04_doseresponse_placebo.py — Part 1 Test 4, the last gate before staking findings.
Dose-response: completion should rise MORE where applied surge rose MORE.
Placebo:       completion should stay FLAT where surge never moved (off-peak/night, ~1.0x),
               sited far from peak (spillover correction E1), read within a fixed
               distance band only (composition correction E4).

Data rules: applied congestion REBUILT from congestion_sum/congestion_n (never the p50).
Completion read as completed/searches AND as raw completed COUNT (Test-5 denominator
discipline). Auto and Auto Priority never blended.
Run: python3 02_Research/04_doseresponse_placebo.py
"""
import pandas as pd, numpy as np

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08","09","10","16","17","18","19","20"}
R["tod"] = R.hour_bucket.map(lambda h: "night" if h == "night(23-06)"
                             else ("peak" if h in peak else "offpeak_mid"))

def rate(d, n, de): return d[n].sum()/d[de].sum() if d[de].sum() else np.nan
def cong(d):        return d.congestion_sum.sum()/d.congestion_n.sum() if d.congestion_n.sum() else np.nan

dist_order = ["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16+"]

print("="*78)
print("[T4-A] DOSE-RESPONSE — 250 vs 252 inside PEAK, per distance band, per tier")
print("       does the band where surge rose more show completion rising more?")
print("="*78)
pk = R[(R.tod=="peak") & (R.pricing_version.isin(["250","252"]))]
for tier in ["Auto","Auto Priority"]:
    print(f"  -- {tier} --   (band: Δcong=252-250 surge ; Δcomp=252-250 comp/search ; n=min searches)")
    T = pk[pk.service_tier==tier]
    rows=[]
    for b in dist_order:
        d250=T[(T.pricing_version=="250")&(T.distance_bucket==b)]
        d252=T[(T.pricing_version=="252")&(T.distance_bucket==b)]
        nmin=min(d250.searches.sum(), d252.searches.sum())
        if nmin < 300: continue
        dc = cong(d252)-cong(d250)
        dcomp = rate(d252,"completed","searches")-rate(d250,"completed","searches")
        rows.append((b,dc,dcomp,nmin))
        print(f"     {b:6s}: Δcong={dc:+.3f}  Δcomp={dcomp:+.3f}  "
              f"(250 comp={rate(d250,'completed','searches'):.3f} cong={cong(d250):.2f} | "
              f"252 comp={rate(d252,'completed','searches'):.3f} cong={cong(d252):.2f})  n={nmin:,.0f}")
    if len(rows)>=3:
        dcs=np.array([r[1] for r in rows]); dcomps=np.array([r[2] for r in rows])
        if dcs.std()>0 and dcomps.std()>0:
            print(f"     corr(Δcong, Δcomp) across bands = {np.corrcoef(dcs,dcomps)[0,1]:+.2f}  "
                  f"(positive = dose-response holds)")

print("\n"+"="*78)
print("[T4-B] DOSE-RESPONSE v2 — bin PEAK cells by applied-surge, within fixed band")
print("       Auto Priority, band 2-3 & 4-5 (most volume); higher surge -> higher comp?")
print("="*78)
for tier in ["Auto Priority","Auto"]:
    for b in ["2-3","4-5","6-7"]:
        d = R[(R.tod=="peak")&(R.service_tier==tier)&(R.distance_bucket==b)].copy()
        d=d[d.congestion_n>0]
        d["cong_cell"]=d.congestion_sum/d.congestion_n
        if d.searches.sum()<2000: continue
        q=d["cong_cell"].quantile([.33,.66]).values
        d["surge_bin"]=np.where(d.cong_cell<=q[0],"lo",np.where(d.cong_cell<=q[1],"mid","hi"))
        line=[]
        for sb in ["lo","mid","hi"]:
            s=d[d.surge_bin==sb]
            if s.searches.sum()==0: continue
            line.append(f"{sb}(cong~{cong(s):.2f}):comp={rate(s,'completed','searches'):.3f}")
        print(f"  {tier:14s} band {b:4s}: " + "  ".join(line))

print("\n"+"="*78)
print("[T4-C] PLACEBO — where surge never moved, did completion still rise PRE->POST?")
print("       night + off-peak-mid, applied cong ~1.0, far from peak (spillover-safe)")
print("       read within fixed distance band; a rising placebo = NOT pricing")
print("="*78)
pre=R[R.date<="2026-06-09"]; post=R[R.date>="2026-06-10"]
for tier in ["Auto","Auto Priority"]:
    print(f"  -- {tier} --")
    for tod in ["night","offpeak_mid"]:
        for b in ["2-3","4-5"]:
            a=pre[(pre.service_tier==tier)&(pre.tod==tod)&(pre.distance_bucket==b)]
            z=post[(post.service_tier==tier)&(post.tod==tod)&(post.distance_bucket==b)]
            if min(a.searches.sum(),z.searches.sum())<500: continue
            print(f"     {tod:11s} {b:4s}: comp/search {rate(a,'completed','searches'):.3f}->"
                  f"{rate(z,'completed','searches'):.3f}  "
                  f"cong {cong(a):.2f}->{cong(z):.2f}  "
                  f"completed/day {a.completed.sum()/23:.0f}->{z.completed.sum()/13:.0f}")

print("\n"+"="*78)
print("[T4-D] RAW COMPLETED COUNT — the metric leadership cares about, by tier & period")
print("       (ratio can rise on a falling denominator; count cannot be faked)")
print("="*78)
for tier in ["Auto","Auto Priority"]:
    d=R[R.service_tier==tier]
    for lbl,lo,hi,days in [("May18-31","2026-05-18","2026-05-31",14),
                           ("Jun01-09","2026-06-01","2026-06-09",9),
                           ("Jun10-22","2026-06-10","2026-06-22",13)]:
        w=d[(d.date>=lo)&(d.date<=hi)]
        print(f"  {tier:14s} {lbl}: completed/day={w.completed.sum()/days:,.0f}  "
              f"searches/day={w.searches.sum()/days:,.0f}  comp/search={rate(w,'completed','searches'):.3f}")
