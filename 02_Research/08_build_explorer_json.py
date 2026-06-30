"""
08_build_explorer_json.py — exports the Part 2 evidence as JSON for the website's
interactive slice explorer. Reuses the EXACT methodology of 04_doseresponse_placebo.py:
  - applied congestion rebuilt from congestion_sum/congestion_n (never the p50)
  - completion read as completed/searches AND raw completed count
  - 250-vs-252 inside PEAK only; Auto and Auto Priority never blended
Output: site/data/explorer.json
Run: python3 02_Research/08_build_explorer_json.py
"""
import pandas as pd, numpy as np, json, os

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08","09","10","16","17","18","19","20"}
R["tod"] = R.hour_bucket.map(lambda h: "night" if h == "night(23-06)"
                             else ("peak" if h in peak else "offpeak_mid"))

def rate(d, n, de):
    return float(d[n].sum()/d[de].sum()) if d[de].sum() else None
def cong(d):
    return float(d.congestion_sum.sum()/d.congestion_n.sum()) if d.congestion_n.sum() else None

dist_order = ["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16+"]
out = {"tiers": {}}

# ---- 1) Dose-response: 250 vs 252 inside peak, per band, per tier ----
pk = R[(R.tod=="peak") & (R.pricing_version.isin(["250","252"]))]
for tier in ["Auto","Auto Priority"]:
    T = pk[pk.service_tier==tier]
    bands=[]
    dcs=[]; dcomps=[]; weights=[]
    for b in dist_order:
        d250=T[(T.pricing_version=="250")&(T.distance_bucket==b)]
        d252=T[(T.pricing_version=="252")&(T.distance_bucket==b)]
        nmin=min(int(d250.searches.sum()), int(d252.searches.sum()))
        if nmin < 300:
            continue
        c250,c252 = cong(d250), cong(d252)
        comp250,comp252 = rate(d250,"completed","searches"), rate(d252,"completed","searches")
        dc = c252-c250
        dcomp = comp252-comp250
        bands.append({
            "band": b,
            "cong_250": round(c250,3), "cong_252": round(c252,3),
            "comp_250": round(comp250,3), "comp_252": round(comp252,3),
            "delta_cong": round(dc,3), "delta_comp": round(dcomp,3),
            "n": nmin,
            "completed_250": int(d250.completed.sum()), "completed_252": int(d252.completed.sum()),
        })
        dcs.append(dc); dcomps.append(dcomp); weights.append(nmin)
    corr = corr_w = None
    if len(dcs)>=3:
        dcs_a, dcomps_a = np.array(dcs), np.array(dcomps)
        if dcs_a.std()>0 and dcomps_a.std()>0:
            corr = round(float(np.corrcoef(dcs_a,dcomps_a)[0,1]),2)
            w = np.array(weights, float); w/=w.sum()
            mx,my = (w*dcs_a).sum(),(w*dcomps_a).sum()
            cov=(w*(dcs_a-mx)*(dcomps_a-my)).sum()
            sx=np.sqrt((w*(dcs_a-mx)**2).sum()); sy=np.sqrt((w*(dcomps_a-my)**2).sum())
            corr_w = round(float(cov/(sx*sy)),2) if sx>0 and sy>0 else None
    out["tiers"][tier] = {"bands": bands, "corr": corr, "corr_weighted": corr_w}

# ---- 2) Raw completed count by tier & period (the metric leadership cares about) ----
periods = [("May 18–31","2026-05-18","2026-05-31",14),
           ("Jun 1–9","2026-06-01","2026-06-09",9),
           ("Jun 10–22 (post-rollout)","2026-06-10","2026-06-22",13)]
raw = {}
for tier in ["Auto","Auto Priority"]:
    d=R[R.service_tier==tier]; rows=[]
    for lbl,lo,hi,days in periods:
        w=d[(d.date>=lo)&(d.date<=hi)]
        rows.append({"period":lbl,
                     "completed_per_day": round(w.completed.sum()/days),
                     "searches_per_day": round(w.searches.sum()/days),
                     "comp_per_search": round(rate(w,"completed","searches"),3)})
    raw[tier]=rows
out["raw_counts"]=raw

# ---- 3) Placebo: surge-flat hours, pre vs post ----
pre=R[R.date<="2026-06-09"]; post=R[R.date>="2026-06-10"]
placebo={}
for tier in ["Auto","Auto Priority"]:
    rows=[]
    for tod,label in [("night","Night (23–06)"),("offpeak_mid","Off-peak midday")]:
        a=pre[(pre.service_tier==tier)&(pre.tod==tod)]
        z=post[(post.service_tier==tier)&(post.tod==tod)]
        rows.append({"window":label,
                     "comp_pre":round(rate(a,"completed","searches"),3),
                     "comp_post":round(rate(z,"completed","searches"),3),
                     "cong_pre":round(cong(a),2),"cong_post":round(cong(z),2)})
    placebo[tier]=rows
out["placebo"]=placebo

os.makedirs("site/data", exist_ok=True)
with open("site/data/explorer.json","w") as f:
    json.dump(out,f,indent=2)
print("wrote site/data/explorer.json")
print(json.dumps({"Auto_corr":out['tiers']['Auto']['corr'],
                  "AutoPriority_corr":out['tiers']['Auto Priority']['corr'],
                  "Auto_bands":len(out['tiers']['Auto']['bands']),
                  "AP_bands":len(out['tiers']['Auto Priority']['bands'])}, indent=2))
