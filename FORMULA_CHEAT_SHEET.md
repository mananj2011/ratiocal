# Formula Cheat Sheet - Quick Reference 📋

**Print this out and keep it next to you during the presentation!**

---

# YOUR KEY NUMBERS (MEMORIZE THESE!)

```
┌─────────────────────────────────────────────────────────┐
│  Portfolio Expected Value:        +27.7%                │
│  Market Edge:                     +22.6% (306%)         │
│  Sortino (You vs Nifty):          0.75 vs 0.51 (1.5x)   │
│  Kelly Multiplier:                0.98x (optimal)       │
│  Correlation:                     0.352 (good)          │
│  Max Drawdown (protected):        -20.7%                │
└─────────────────────────────────────────────────────────┘
```

---

# METRIC 1: EXPECTED VALUE

**What it is:** Average return if you ran this 100 times

**Formula:**
```
EV = Σ (Probability × Return)
   = (P₁ × R₁) + (P₂ × R₂) + (P₃ × R₃)
```

**Your calculation:**

**RPOWER:**
```
Bull:  30% × 90%  = 0.30 × 0.90 = +0.270
Mixed: 50% × 15%  = 0.50 × 0.15 = +0.075
Bear:  20% × -40% = 0.20 × -0.40 = -0.080
                                    -------
EV (RPOWER) = +0.265 = +26.5%
```

**SURYA:**
```
Base:  60% × 27%  = 0.60 × 0.27 = +0.162
Bull:  25% × 64%  = 0.25 × 0.64 = +0.160
Bear:  15% × -18% = 0.15 × -0.18 = -0.027
                                    -------
EV (SURYA) = +0.295 = +29.5%
```

**PORTFOLIO:**
```
Portfolio EV = (60% × 26.5%) + (40% × 29.5%)
             = (0.60 × 0.265) + (0.40 × 0.295)
             = 0.159 + 0.118
             = 0.277 = +27.7%
```

**One-liner:**
> "Our portfolio has a +27.7% Expected Value - that's what we'd average if we ran this 100 times."

---

# METRIC 2: KELLY CRITERION

**What it is:** Mathematically optimal position size

**Simplified Formula:**
```
Kelly % = (Win Prob × Win Return - Loss Prob × Loss Return) / Win Return
```

**Your calculation (RPOWER):**

**Step 1:** Win scenarios
```
Bull + Mixed = 30% + 50% = 80% win probability
```

**Step 2:** Average win return
```
Weighted avg = [(30% × 90%) + (50% × 15%)] / 80%
             = [27% + 7.5%] / 80%
             = 34.5% / 80%
             = 43.1%
```

**Step 3:** Loss scenario
```
Loss probability = 20%
Loss return = 40% (absolute)
```

**Step 4:** Apply formula
```
Kelly = (80% × 43.1% - 20% × 40%) / 43.1%
      = (34.5% - 8%) / 43.1%
      = 26.5% / 43.1%
      = 61.4%
```

**Your allocation:** 60% (0.98x Kelly - essentially optimal!)

**One-liner:**
> "Kelly Criterion says allocate 61% to RPOWER. We're using 60% - that's 0.98x Kelly, essentially optimal for this 9-month horizon."

---

# METRIC 3: SORTINO RATIO

**What it is:** Risk-adjusted return (penalizes ONLY downside)

**Formula:**
```
Sortino = (Portfolio Return - Risk-Free Rate) / Downside Deviation

Where:
- Portfolio Return = Average daily return × 252 (annualized)
- Risk-Free Rate = 7% / 252 per day
- Downside Deviation = Std dev of ONLY negative returns × √252
```

**Why use it:**
- Sharpe penalizes ALL volatility (good and bad)
- Sortino penalizes ONLY bad volatility (losses)
- For asymmetric strategies (big upside, limited downside), Sortino is correct

**Your numbers:**
```
Portfolio Sortino: 0.75
Nifty Sortino:     0.51
Advantage:         1.5x (50% better)
```

**One-liner:**
> "Our Sortino is 0.75 vs Nifty's 0.51 - we're getting 1.5x better risk-adjusted returns because we only penalize downside risk, not upside potential."

---

# METRIC 4: SHARPE RATIO

**What it is:** Traditional risk-adjusted return (penalizes ALL volatility)

**Formula:**
```
Sharpe = (Portfolio Return - Risk-Free Rate) / Total Standard Deviation

Where:
- Total Standard Deviation = Std dev of ALL returns (up and down) × √252
```

**Why we show it:**
To prove why it's WRONG for this strategy

**Your numbers:**
```
Portfolio Sharpe: 0.41
Nifty Sharpe:     0.32
Advantage:        1.3x
```

**The comparison:**
```
Metric      | You  | Nifty | Advantage
------------|------|-------|----------
Sharpe      | 0.41 | 0.32  | 1.3x
Sortino     | 0.75 | 0.51  | 1.5x
```

**See how gap widens?** Sortino correctly identifies upside volatility as GOOD.

**One-liner:**
> "Our Sharpe is 0.41 vs Nifty's 0.32 - we're better even by traditional metrics. But Sharpe understates our edge because it penalizes our +90% upside potential. That's why we focus on Sortino."

---

# METRIC 5: IMPLIED PROBABILITY

**What it is:** What probability the market is assigning to your bull case

**Formula (Black-Scholes d2):**
```
d2 = [ln(S/K) + (r - 0.5σ²)T] / (σ√T)

Market Implied Prob = N(d2)

Where:
S = Current price (₹41.33)
K = Target price (₹78.53)
r = Risk-free rate (7% = 0.07)
σ = Volatility (56.6% = 0.566)
T = Time in years (9 months = 0.75)
N(d2) = Normal cumulative distribution function
```

**Your calculation:**
```
d2 = [ln(41.33/78.53) + (0.07 - 0.5×0.566²)×0.75] / (0.566×√0.75)
   = [ln(0.526) + (0.07 - 0.160)×0.75] / (0.566×0.866)
   = [-0.642 + (-0.068)] / 0.490
   = -0.710 / 0.490
   = -1.449

N(-1.449) = 7.4%
```

**Your numbers:**
```
Market implies:    7.4%
You assessed:     30.0%
Edge:            +22.6%
Mispricing:       306%
```

**One-liner:**
> "The market prices RPOWER as if there's only a 7.4% chance of our bull case. We think it's 30%. That's a 22.6% edge - a 306% mispricing."

---

# METRIC 6: CORRELATION

**What it is:** Do your stocks move together or independently?

**Formula:**
```
Correlation = Covariance(Stock A, Stock B) / (StdDev(A) × StdDev(B))

Or in Excel: =CORREL(A_returns, B_returns)
```

**How to interpret:**
```
1.0:       Perfect correlation (always move together) ❌
0.7-1.0:   High correlation (usually move together) ⚠️
0.3-0.7:   Moderate correlation (sometimes together) ✅
0-0.3:     Low correlation (rarely together) ✅✅
-1.0:      Perfect inverse (when one up, other down)
```

**Your number:** 0.352 (good diversification)

**What this means:**
When RPOWER crashes on legal news → SURYA unaffected
Different industries, different catalysts = TRUE diversification

**One-liner:**
> "Correlation is 0.352 - when RPOWER faces legal delays, SURYA is unaffected. True diversification across independent catalysts."

---

# METRIC 7: MAXIMUM DRAWDOWN

**What it is:** Worst peak-to-trough loss

**Formula:**
```
For each day:
  Drawdown = (Current Value - Peak Value) / Peak Value

Maximum Drawdown = Most negative drawdown in the period
```

**Your numbers:**
```
Historical max:        -35.8% (from actual data)
Scenario worst-case:   -31.2% (both stocks bear)
With stop-loss:        -20.7% (protected)
```

**Scenario calculation:**
```
If both hit bear case:
= (60% × -40%) + (40% × -18%)
= -24% + -7.2%
= -31.2%

With stop-loss at ₹32:
RPOWER loss = (32 - 41.33) / 41.33 = -22.6%
= (60% × -22.6%) + (40% × -18%)
= -13.6% + -7.2%
= -20.7%
```

**One-liner:**
> "Worst-case is -31.2% if both stocks hit bear scenarios. But our ₹32 stop-loss for RPOWER caps it at -20.7% while keeping full upside."

---

# QUICK CONVERSION FORMULAS

**Percentage to Decimal:**
```
30% → 0.30
7.4% → 0.074
```

**Decimal to Percentage:**
```
0.277 → 27.7%
0.074 → 7.4%
```

**Calculate percentage change:**
```
% Change = (New - Old) / Old

Example:
Price went from ₹41.33 to ₹78.53
= (78.53 - 41.33) / 41.33
= 37.20 / 41.33
= 0.90 = 90%
```

**Weighted average:**
```
60% × A + 40% × B
= (0.60 × A) + (0.40 × B)

Example:
60% × 26.5% + 40% × 29.5%
= (0.60 × 0.265) + (0.40 × 0.295)
= 0.159 + 0.118
= 0.277 = 27.7%
```

---

# EXCEL FORMULAS (IF NEEDED)

**Expected Value:**
```excel
=SUMPRODUCT(Probabilities, Returns)

Example:
=SUMPRODUCT(B2:B4, C2:C4)
Where B2:B4 = {30%, 50%, 20%}
      C2:C4 = {90%, 15%, -40%}
Result: 26.5%
```

**Correlation:**
```excel
=CORREL(Stock1_Returns, Stock2_Returns)

Example:
=CORREL(A2:A248, B2:B248)
```

**Standard Deviation:**
```excel
=STDEV.P(Returns_Range) * SQRT(252)

For daily returns, multiply by √252 to annualize
```

**Sortino (downside deviation):**
```excel
1. Filter for negative returns only
2. =STDEV.P(Negative_Returns) * SQRT(252)
3. Sortino = (Avg_Return * 252 - RiskFree) / Downside_Dev
```

---

# SCENARIO REFERENCE TABLE

**Your exact scenarios for RPOWER:**

| Scenario | Probability | Return | Contribution |
|----------|-------------|--------|--------------|
| Bull     | 30%         | +90%   | +27.0%       |
| Mixed    | 50%         | +15%   | +7.5%        |
| Bear     | 20%         | -40%   | -8.0%        |
| **Total EV** | **100%** | —      | **+26.5%**   |

**Your exact scenarios for SURYA:**

| Scenario | Probability | Return | Contribution |
|----------|-------------|--------|--------------|
| Base     | 60%         | +27%   | +16.2%       |
| Bull     | 25%         | +64%   | +16.0%       |
| Bear     | 15%         | -18%   | -2.7%        |
| **Total EV** | **100%** | —      | **+29.5%**   |

---

# COMMON CALCULATION MISTAKES TO AVOID

❌ **Mistake 1:** Forgetting to convert percentages to decimals
```
WRONG: 30% × 90% = 2700%
RIGHT: 0.30 × 0.90 = 0.27 = 27%
```

❌ **Mistake 2:** Adding percentages instead of weighting
```
WRONG: 26.5% + 29.5% = 56% (portfolio EV)
RIGHT: (60% × 26.5%) + (40% × 29.5%) = 27.7%
```

❌ **Mistake 3:** Using simple average instead of weighted
```
WRONG: (26.5% + 29.5%) / 2 = 28%
RIGHT: 0.60 × 26.5% + 0.40 × 29.5% = 27.7%
```

❌ **Mistake 4:** Forgetting probabilities must sum to 100%
```
CHECK: 30% + 50% + 20% = 100% ✓
```

---

# THE 30-SECOND ELEVATOR PITCH

If someone says "Explain your strategy in 30 seconds":

> "We have a quantifiable edge. The market is pricing Reliance Power at a 7.4% probability for our bull case - we think it's 30%. That's a 22.6% edge. We've sized our positions using Kelly Criterion at optimal 60/40 allocation. Our portfolio has a +27.7% Expected Value with risk-adjusted returns 1.5x better than Nifty using Sortino Ratio. We have true diversification with 0.352 correlation, and we've capped downside at -20.7% via stop-loss while maintaining full upside. We think like poker players, size positions like Kelly, and use Sortino instead of Sharpe. We have the math to prove it."

---

# PRE-PRESENTATION VERBAL PRACTICE

**Say these out loud 5 times each:**

1. "Our Expected Value is twenty-seven point seven percent"
2. "We have a twenty-two point six percent edge over market pricing"
3. "Our Sortino Ratio is zero point seven five versus Nifty's zero point five one"
4. "That's one point five times better risk-adjusted returns"
5. "Kelly Criterion says sixty-one percent, we're using sixty percent"
6. "Correlation is zero point three five two - good diversification"
7. "Maximum drawdown is capped at twenty point seven percent with stop-loss"

**Practice the full sequence:**
> "Expected Value: twenty-seven point seven percent. Market edge: twenty-two point six percent. Sortino: zero point seven five versus zero point five one. That's one point five times better. Kelly optimal: sixty percent. Correlation: zero point three five two. Max drawdown: twenty point seven percent."

---

# FINAL CHECKLIST

**Before you present:**
- [ ] All probabilities sum to 100% (RPOWER: 30+50+20=100 ✓, SURYA: 60+25+15=100 ✓)
- [ ] All allocations sum to 100% (60+40=100 ✓)
- [ ] Know your three key numbers by heart (+27.7%, +22.6%, 0.75 vs 0.51)
- [ ] Calculator nearby (in case they ask you to recalculate something)
- [ ] This cheat sheet printed out
- [ ] Deep breath

**You've got this!** 🎯
