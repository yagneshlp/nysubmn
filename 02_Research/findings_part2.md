# 02 — Part 2 Findings (running the Part 1 five-test ladder on real slices)

*Source: `03_competitor_defection.py` (+ `01`/`02` from the sanity pass). Additive cols rebuilt;
no frozen quantile averaged. Auto and Auto Priority never blended.*

## Test 5, competitor guard — RUN. The rider-price-defection alternative is ruled out.

Part 1 made the competitor check a gate, not a footnote, and it guards both ends: NY priced too
high (riders defect at Stage 1) or the rival's fare high enough to out-bid NY for the driver (poach
at Stage 3). The data settles which end is live.

**CG1 — NY is the cheap option, not the expensive one, in every distance band, both periods.**
Comparing avg fare per trip *within band* (rebuilt additive `fare_sum/fare_n`, NOT a per-km median),
NY Auto runs **5–33% below** the cheaper rival. The discount is largest exactly on short trips
(1-2 km: −33% PRE, −23% POST) and shrinks with distance. Riders were never pushed toward Uber/Ola
because NY got expensive; NY stayed materially cheaper throughout. The Stage-1 price-defection risk
H4 flagged is **not borne out on price**. (Whether riders left on ETA is unobserved — NY's
`eta_min_p50` is absent from the scrape, logged as 0.)

**STRUCTURAL — flat pass-through vs commission reframes the whole competitor read.** NY is
zero-commission: rider fare = driver take, one number. Rivals run commission + subsidy, which
DECOUPLES rider price from driver payout (charge rider ₹100, keep a cut, still pay driver ₹90 off
balance sheet). Two consequences: (a) the scrape shows the rider side only; we CANNOT infer the
driver-side economics that govern the poach — honest gap. (b) The charge is the ONLY dial NY has on
driver pay and every rupee comes 1:1 from the rider, so it hits Stage-1 price-sensitivity instantly
and cannot outbid a subsidy. This is the structural floor under H1 and almost certainly why the AP
dose-response saturates near 1.5x (surge fully visible to rider under flat pass-through).

**CG2 — Across the rollout NY drifted *cheaper* relative to rivals, not dearer — the opposite of
"surge priced us up."** Auto Priority peak NY-vs-rival ppk gap widened from −10% to −18%; off-peak
−9% to −14%. Even where the congestion surge applied, the rival's rider-fare sits far above NY's.
That headroom is the H1 poach mechanism made concrete: the competitor charges the rider more and can
hand the driver more, and NY's ~₹8 bump cannot close a gap that wide under zero-commission. The live
competitor risk is **driver poach at Stage 3, not rider defection at Stage 1.**

**CG3 — The one place NY moved toward rivals is the one place H3 predicted surge would bite.** Short
Auto trips narrowed from −33% to −23% (still cheaper, just less so). That is the congestion charge
doing its narrow intended job on short peak trips, not pricing NY out of the market.

## How this maps to the ladder
- **Test 1 (did price move):** surge barely moved on Auto (1.062→1.068) [F1]; moved on Auto
  Priority. CG3 confirms the move is concentrated on short trips.
- **Test 3 (250 vs 252 in peak):** the only honest pricing read; small Auto edge not surge-driven,
  real Auto Priority edge with more surge [F6] — now survives the CG2 poach check as *demand had
  nowhere cheaper to go*, so the Priority edge is more credible than F6 left it.
- **Test 5 (competitor guard):** DONE here. Rider-defection ruled out; poach is the live risk.

## Test 4 (dose-response + placebo) — RUN. The two tiers split cleanly.

**DR1 — Auto (mass tier): surge and completion are INVERSELY related. Dose-response fails.**
- 250-vs-252 in peak: 252 completes +0.02 to +0.04 better in every band, but with EQUAL-or-LOWER
  surge (Δcong ≈ 0 to −0.008) and a lower avg fare (152 vs 154). corr(Δcong,Δcomp) across bands
  = **−0.72**. 252's edge is real but it is NOT the congestion charge.
- Binning peak Auto cells by applied surge within fixed band: more surge → LESS completion
  (band 4-5: cong 1.03→0.518, 1.10→0.432, 1.14→0.372). On Auto the charge is a congestion
  *thermometer*, not a completion *medicine*: it fires when the market is already stressed.

**DR2 — Auto Priority: dose-response HOLDS, but bounded by a saturation ceiling.**
- 250-vs-252 in peak: the bands where 252 added the most surge are exactly the bands where
  completion rose most (4-5: cong 1.41→1.52, comp 0.770→0.890, +0.121; 9-10: +0.145 on +0.094
  cong); long bands where surge didn't move (12-16, 16+) show no lift. corr = **+0.80**.
- BUT within-band surge bins are an inverted-U: comp lo→mid RISES (0.65→0.81) then mid→hi FALLS
  (0.81→0.64 at ~1.6x). Real effect, real ceiling: push past ~1.5x and it backfires.

**PL — Placebo LIGHTS UP. The headline lift is mostly not pricing.**
- Off-peak & night Auto, where surge ~flat, completion rose just as much as peak (night 2-3:
  0.335→0.437; offpeak 2-3: 0.430→0.522). A lever that only acts at surge cannot move no-surge hours.
- Raw completed/day (cannot be faked by a denominator): Auto **82.9k→88.9k BEFORE rollout→91.8k**
  after, on a FALLING search base (181k→168k). Auto Priority completed/day **FELL** post-rollout
  (16.9k→15.9k, window low) even as its ratio "rose" 0.664→0.767 — pure shrinking denominator
  (searches 25.4k→20.8k).

## The two reputation-grade findings (staked)
1. **The credible narrow win:** AP-in-peak v252 pricing genuinely converts — clean +0.80 dose-
   response, competitor gate clears, bounded by a ~1.5x saturation ceiling. Small, specific, real.
2. **The headline does NOT survive:** the +14.9% is inverse-dosed on Auto, lights up the placebo,
   and dissolves on raw counts (recovery pre-dates rollout; AP completed rides fell). Mostly
   demand recovery + falling search denominator, credited to pricing because timing lined up.
