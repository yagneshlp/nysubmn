"""
05_plots.py — Figures for Part 2. Self-contained; rebuilds every number from the cube
under the same rules (additive sums; congestion rebuilt from sum/n; tiers never blended).
Outputs PNGs to 02_Research/plots/.

WHY EACH FIGURE EXISTS:
  fig1_dose_response  — The core causal test (Test 4). Plots Δsurge vs Δcompletion across
      distance bands, 250-vs-252 inside peak. The sign-flip between Auto (r=−0.72, more
      surge → LESS completion) and Auto Priority (r=+0.80) is the most decision-relevant
      chart: opposite effects by tier, ruling out any general "pricing fixed it" narrative.

  fig2_saturation  — Auto Priority completion rises with surge up to ~1.5x then inverts.
      This is why "scale the charge" is the wrong lever even where it works; there is a
      ceiling baked into the mechanism, likely driver-supply saturation.

  fig3_placebo  — Off-peak and night completion rose as much as peak even though surge
      barely moved there. A peak-only lever cannot explain a system-wide lift. This is the
      visual proof behind Finding 2: something else — version swap, matching improvement —
      drove the off-peak gain, not the congestion charge.

  fig4_count_vs_ratio  — Ratio rose but raw rides per day flat/fell while searches fell
      faster. This is the denominator discipline chart: the metric leadership cares about
      is rides completed, not a ratio on a shrinking search base.

  fig5_competitor_gap  — NY is the cheapest option in every distance band. Rider price-
      defection (Stage-1 risk) is ruled out. Also shows why the charge saturates: flat
      fare = driver take, rivals can subsidise separately from their commission margin.

Run: python3 02_Research/05_plots.py
"""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.grid": True,
    "grid.alpha": 0.25, "axes.spines.top": False, "axes.spines.right": False,
})
NY, RIV1, GREY = "#1b9e77", "#d95f02", "#7570b3"
OUT = "02_Research/plots"

R = pd.read_csv("data/rides.csv", dtype={"pricing_version": str, "hour_bucket": str})
peak = {"08","09","10","16","17","18","19","20"}
R["tod"] = R.hour_bucket.map(lambda h: "night" if h == "night(23-06)"
                             else ("peak" if h in peak else "offpeak"))
def rate(d,n,de): return d[n].sum()/d[de].sum() if d[de].sum() else np.nan
def cong(d): return d.congestion_sum.sum()/d.congestion_n.sum() if d.congestion_n.sum() else np.nan
dist = ["0-1","1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16+"]

# ---------- FIG 1: dose-response, 250 vs 252 in peak, per band, both tiers ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
pk = R[(R.tod=="peak") & (R.pricing_version.isin(["250","252"]))]
for ax, tier, col in [(axes[0],"Auto",RIV1),(axes[1],"Auto Priority",NY)]:
    T = pk[pk.service_tier==tier]; xs,ys=[],[]
    for b in dist:
        a=T[(T.pricing_version=="250")&(T.distance_bucket==b)]
        c=T[(T.pricing_version=="252")&(T.distance_bucket==b)]
        if min(a.searches.sum(),c.searches.sum())<300: continue
        xs.append(cong(c)-cong(a)); ys.append(rate(c,"completed","searches")-rate(a,"completed","searches"))
    xs,ys=np.array(xs),np.array(ys)
    ax.axhline(0,color="grey",lw=.8); ax.axvline(0,color="grey",lw=.8)
    ax.scatter(xs,ys,s=70,color=col,zorder=3,edgecolor="white")
    m,b0=np.polyfit(xs,ys,1); xr=np.linspace(xs.min(),xs.max(),50)
    ax.plot(xr,m*xr+b0,"--",color=col,alpha=.7)
    r=np.corrcoef(xs,ys)[0,1]
    ax.set_title(f"{tier}\nmore surge → {'MORE' if r>0 else 'LESS'} completion   (r = {r:+.2f})")
    ax.set_xlabel("Δ applied surge  (252 − 250)")
    ax.xaxis.set_major_formatter(PercentFormatter(1.0,decimals=1))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0,decimals=0))
axes[0].set_ylabel("Δ completion-per-search  (252 − 250)")
fig.suptitle("Dose-response (Test 4): does the surge dial move completion?  250 vs 252, peak, by distance band",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(f"{OUT}/fig1_dose_response.png"); plt.close(fig)

# ---------- FIG 2: surge saturation, completion by applied-surge bin within band ----------
fig, ax = plt.subplots(figsize=(8.5,5.2))
bands=["2-3","4-5","6-7"]
for tier,col,mk in [("Auto Priority",NY,"o"),("Auto",RIV1,"s")]:
    bin_means={"lo":[],"mid":[],"hi":[]}; bin_cong={"lo":[],"mid":[],"hi":[]}
    for b in bands:
        d=R[(R.tod=="peak")&(R.service_tier==tier)&(R.distance_bucket==b)].copy()
        d=d[d.congestion_n>0]; d["cc"]=d.congestion_sum/d.congestion_n
        q=d.cc.quantile([.33,.66]).values
        d["sb"]=np.where(d.cc<=q[0],"lo",np.where(d.cc<=q[1],"mid","hi"))
        for sb in ["lo","mid","hi"]:
            s=d[d.sb==sb]; bin_means[sb].append(rate(s,"completed","searches")); bin_cong[sb].append(cong(s))
    x=[np.mean(bin_cong[sb]) for sb in ["lo","mid","hi"]]
    y=[np.mean(bin_means[sb]) for sb in ["lo","mid","hi"]]
    ax.plot(x,y,mk+"-",color=col,ms=10,lw=2,label=tier)
    for xi,yi,lab in zip(x,y,["low","mid","high"]): ax.annotate(lab,(xi,yi),textcoords="offset points",xytext=(6,6),fontsize=9)
ax.set_title("Surge saturation (Test 4): completion vs surge actually applied\nAuto Priority inverts past ~1.5x; Auto declines throughout")
ax.set_xlabel("applied congestion multiplier (rebuilt, within fixed distance band)")
ax.set_ylabel("completion-per-search"); ax.yaxis.set_major_formatter(PercentFormatter(1.0,decimals=0))
ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig2_saturation.png"); plt.close(fig)

# ---------- FIG 3: placebo, completion PRE vs POST by time-of-day (Auto) ----------
fig, ax = plt.subplots(figsize=(8.5,5.2))
pre=R[R.date<="2026-06-09"]; post=R[R.date>="2026-06-10"]
tods=["peak","offpeak","night"]; A=lambda df,t: df[(df.service_tier=="Auto")&(df.tod==t)]
prev=[rate(A(pre,t),"completed","searches") for t in tods]
postv=[rate(A(post,t),"completed","searches") for t in tods]
x=np.arange(len(tods)); w=.36
ax.bar(x-w/2,prev,w,label="PRE (May18–Jun9)",color=GREY,alpha=.85)
ax.bar(x+w/2,postv,w,label="POST (Jun10–22)",color=NY,alpha=.9)
for i,(a,b) in enumerate(zip(prev,postv)):
    ax.text(i,b+.008,f"+{(b/a-1)*100:.0f}%",ha="center",fontsize=10,fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(["PEAK\n(surge fires)","OFF-PEAK\n(≈no surge)","NIGHT\n(≈no surge)"])
ax.set_title("Placebo (Test 4): Auto completion rose as much where surge never moved\nA peak-only lever cannot explain off-peak & night gains",fontsize=11.5)
ax.set_ylabel("completion-per-search"); ax.yaxis.set_major_formatter(PercentFormatter(1.0,decimals=0))
ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig3_placebo.png"); plt.close(fig)

# ---------- FIG 4: ratio rose while the count tells the truth (per tier) ----------
fig, axes = plt.subplots(1,2,figsize=(13,5.4))
wins=[("May18–31","2026-05-18","2026-05-31",14),("Jun1–9","2026-06-01","2026-06-09",9),
      ("Jun10–22\n(rollout)","2026-06-10","2026-06-22",13)]
for ax,tier in zip(axes,["Auto","Auto Priority"]):
    d=R[R.service_tier==tier]; comp,srch,ratio=[],[],[]
    for lbl,lo,hi,days in wins:
        w=d[(d.date>=lo)&(d.date<=hi)]
        comp.append(w.completed.sum()/days); srch.append(w.searches.sum()/days); ratio.append(rate(w,"completed","searches"))
    x=np.arange(3)
    ax.bar(x-.2,comp,.4,label="completed rides/day",color=NY,alpha=.9)
    ax.bar(x+.2,srch,.4,label="searches/day",color=GREY,alpha=.55)
    ax2=ax.twinx(); ax2.plot(x,ratio,"D-",color=RIV1,lw=2.5,ms=9,label="completion/search (ratio)")
    ax2.set_ylim(min(ratio)*.9,max(ratio)*1.08); ax2.yaxis.set_major_formatter(PercentFormatter(1.0,decimals=0))
    ax2.spines.top.set_visible(False)
    for i,r in enumerate(ratio): ax2.text(i,r,f" {r*100:.1f}%",color=RIV1,fontsize=9,fontweight="bold",va="bottom")
    ax.set_xticks(x); ax.set_xticklabels([w[0] for w in wins])
    ax.set_title(f"{tier}: the ratio climbs on a falling denominator"); ax.set_ylabel("rides / searches per day")
    if tier=="Auto Priority": ax.legend(loc="upper left",fontsize=9); ax2.legend(loc="upper right",fontsize=9)
fig.suptitle("Test 4 (raw count): completion-ratio up, but completed rides flat (Auto) / DOWN (Auto Priority) as searches fall",
             fontsize=12.5,fontweight="bold")
fig.tight_layout(rect=[0,0,1,.95]); fig.savefig(f"{OUT}/fig4_count_vs_ratio.png"); plt.close(fig)

# ---------- FIG 5: competitor price gap by distance band (Auto, POST) ----------
C=pd.read_csv("data/competitor_fares.csv",dtype={"hour_bucket":str,"distance_bucket":str})
for c in ["fare_sum","price_per_km_p50"]: C[c]=pd.to_numeric(C[c],errors="coerce")
fig, ax = plt.subplots(figsize=(9.5,5.2))
cb=["1-2","2-3","3-4","4-5","5-6","6-7","7-8","8-9","9-10","10-12","12-16","16-48"]
post_c=C[(C.vehicle=="Auto")&(C.date>="2026-06-10")]
def ppk(df):
    fn=df.fare_n.sum() if "fare_n" in df else 0
    return df.fare_sum.sum()/fn if fn else np.nan
for v,col,lab in [("namma_yatri",NY,"Namma Yatri"),("competitor1",RIV1,"Competitor 1"),("competitor2",GREY,"Competitor 2")]:
    ys=[]
    for b in cb:
        cell=post_c[(post_c.competitor==v)&(post_c.distance_bucket==b)]
        ys.append(ppk(cell) if cell.serviceable_n.sum()>=20 else np.nan)
    ax.plot(cb,ys,"o-",color=col,lw=2,ms=6,label=lab)
ax.set_title("Competitor guard (Test 5): NY is the cheap rider option in every band\nRider price-defection ruled out; flat fare = driver take, so driver side stays unseen",fontsize=11.5)
ax.set_xlabel("distance band (km)"); ax.set_ylabel("avg fare per trip  (₹, rebuilt within band)")
ax.legend(); fig.tight_layout(); fig.savefig(f"{OUT}/fig5_competitor_gap.png"); plt.close(fig)

print("Saved 5 figures to", OUT)
import os
for f in sorted(os.listdir(OUT)): print("  ", f)
