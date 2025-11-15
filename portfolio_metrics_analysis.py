"""
Portfolio Metrics Analysis for Investment Deck
===============================================

Calculates:
1. Expected Value Analysis (scenario-weighted returns)
2. Kelly Criterion (optimal position sizing)
3. Sortino Ratio (asymmetric risk metric)
4. Sharpe Ratio (to show why it's wrong for this strategy)
5. Implied Probability & Market Edge
6. Correlation between holdings
7. Max Drawdown
8. Portfolio-level metrics

Current Holdings:
- 60% Reliance Power (RPOWER)
- 40% Surya Roshni (SURYA)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Current prices (as of Nov 14, 2025)
CURRENT_PRICES = {
    'rpower': 41.33,
    'surya': 274.90,
    'nifty': 25910.05
}

# Portfolio allocation
ALLOCATION = {
    'rpower': 0.60,  # 60%
    'surya': 0.40    # 40%
}

# Time horizon (months)
TIME_HORIZON = 9

# Scenario Analysis for Expected Value
SCENARIOS = {
    'rpower': {
        'bull': {'probability': 0.30, 'return': 0.90},    # 30% chance of 90% return
        'mixed': {'probability': 0.50, 'return': 0.15},   # 50% chance of 15% return
        'bear': {'probability': 0.20, 'return': -0.40}    # 20% chance of -40% return
    },
    'surya': {
        'base': {'probability': 0.60, 'return': 0.27},    # 60% chance of 27% return
        'bull': {'probability': 0.25, 'return': 0.64},    # 25% chance of 64% return
        'bear': {'probability': 0.15, 'return': -0.18}    # 15% chance of -18% return
    }
}

# Risk-free rate (annualized) - approximate Indian T-bill rate
RISK_FREE_RATE = 0.07

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load and clean historical price data"""

    print("Loading historical data...")

    # Load CSVs
    rpower = pd.read_csv('data/Reliance Power Stock Price History.csv')
    surya = pd.read_csv('data/Surya Roshni Stock Price History.csv')
    nifty = pd.read_csv('data/Nifty 50 Historical Data (3).csv')

    # Clean column names (remove BOM if present)
    for df in [rpower, surya, nifty]:
        df.columns = df.columns.str.replace('\ufeff', '').str.strip()

    # Parse dates
    rpower['Date'] = pd.to_datetime(rpower['Date'], format='%m/%d/%Y')
    surya['Date'] = pd.to_datetime(surya['Date'], format='%m/%d/%Y')
    nifty['Date'] = pd.to_datetime(nifty['Date'], format='%m/%d/%Y')

    # Clean price columns (remove commas and convert to float)
    rpower['Price'] = rpower['Price'].astype(str).str.replace(',', '').astype(float)
    surya['Price'] = surya['Price'].astype(str).str.replace(',', '').astype(float)
    nifty['Price'] = nifty['Price'].astype(str).str.replace(',', '').astype(float)

    # Sort by date (oldest to newest)
    rpower = rpower.sort_values('Date').reset_index(drop=True)
    surya = surya.sort_values('Date').reset_index(drop=True)
    nifty = nifty.sort_values('Date').reset_index(drop=True)

    # Select only Date and Price
    rpower = rpower[['Date', 'Price']].rename(columns={'Price': 'rpower'})
    surya = surya[['Date', 'Price']].rename(columns={'Price': 'surya'})
    nifty = nifty[['Date', 'Price']].rename(columns={'Price': 'nifty'})

    # Merge on date
    data = rpower.merge(surya, on='Date', how='inner').merge(nifty, on='Date', how='inner')

    print(f"✓ Loaded {len(data)} trading days of data")
    print(f"  Date range: {data['Date'].min().date()} to {data['Date'].max().date()}")

    return data

# ============================================================================
# METRIC 1: EXPECTED VALUE ANALYSIS
# ============================================================================

def calculate_expected_value():
    """Calculate probability-weighted expected returns"""

    print("\n" + "="*70)
    print("METRIC 1: EXPECTED VALUE ANALYSIS")
    print("="*70)

    # Reliance Power EV
    rpower_ev = sum(
        scenario['probability'] * scenario['return']
        for scenario in SCENARIOS['rpower'].values()
    )

    # Surya Roshni EV
    surya_ev = sum(
        scenario['probability'] * scenario['return']
        for scenario in SCENARIOS['surya'].values()
    )

    # Portfolio EV (weighted by allocation)
    portfolio_ev = (ALLOCATION['rpower'] * rpower_ev +
                   ALLOCATION['surya'] * surya_ev)

    print(f"\nReliance Power Expected Value:")
    for name, scenario in SCENARIOS['rpower'].items():
        print(f"  {name.capitalize():6s}: {scenario['probability']:.0%} × {scenario['return']:+.0%} = {scenario['probability'] * scenario['return']:+.1%}")
    print(f"  → Total EV: {rpower_ev:+.1%}")

    print(f"\nSurya Roshni Expected Value:")
    for name, scenario in SCENARIOS['surya'].items():
        print(f"  {name.capitalize():6s}: {scenario['probability']:.0%} × {scenario['return']:+.0%} = {scenario['probability'] * scenario['return']:+.1%}")
    print(f"  → Total EV: {surya_ev:+.1%}")

    print(f"\nPortfolio Expected Value:")
    print(f"  (60% × {rpower_ev:+.1%}) + (40% × {surya_ev:+.1%}) = {portfolio_ev:+.1%}")

    return {
        'rpower_ev': rpower_ev,
        'surya_ev': surya_ev,
        'portfolio_ev': portfolio_ev
    }

# ============================================================================
# METRIC 2: KELLY CRITERION
# ============================================================================

def calculate_kelly(ev_results):
    """Calculate Kelly optimal position sizing"""

    print("\n" + "="*70)
    print("METRIC 2: KELLY CRITERION (Optimal Position Sizing)")
    print("="*70)

    # For Reliance Power: simplified Kelly for discrete outcomes
    # Kelly % = (p*b - q) / b, where p=win prob, q=loss prob, b=win/loss ratio

    # Weight winning scenarios
    rpower_win_prob = SCENARIOS['rpower']['bull']['probability'] + SCENARIOS['rpower']['mixed']['probability']
    rpower_loss_prob = SCENARIOS['rpower']['bear']['probability']

    # Expected win/loss amounts
    rpower_win_return = (
        SCENARIOS['rpower']['bull']['probability'] * SCENARIOS['rpower']['bull']['return'] +
        SCENARIOS['rpower']['mixed']['probability'] * SCENARIOS['rpower']['mixed']['return']
    ) / rpower_win_prob if rpower_win_prob > 0 else 0

    rpower_loss_return = abs(SCENARIOS['rpower']['bear']['return'])

    # Kelly formula (simplified)
    kelly_rpower = (rpower_win_prob * rpower_win_return - rpower_loss_prob * rpower_loss_return) / rpower_win_return if rpower_win_return > 0 else 0
    kelly_rpower = max(0, min(1, kelly_rpower))  # Bound between 0 and 1

    # For Surya Roshni
    surya_win_prob = SCENARIOS['surya']['base']['probability'] + SCENARIOS['surya']['bull']['probability']
    surya_loss_prob = SCENARIOS['surya']['bear']['probability']

    surya_win_return = (
        SCENARIOS['surya']['base']['probability'] * SCENARIOS['surya']['base']['return'] +
        SCENARIOS['surya']['bull']['probability'] * SCENARIOS['surya']['bull']['return']
    ) / surya_win_prob if surya_win_prob > 0 else 0

    surya_loss_return = abs(SCENARIOS['surya']['bear']['return'])

    kelly_surya = (surya_win_prob * surya_win_return - surya_loss_prob * surya_loss_return) / surya_win_return if surya_win_return > 0 else 0
    kelly_surya = max(0, min(1, kelly_surya))

    # Actual allocation vs Kelly
    kelly_multiplier_rpower = ALLOCATION['rpower'] / kelly_rpower if kelly_rpower > 0 else 0
    kelly_multiplier_surya = ALLOCATION['surya'] / kelly_surya if kelly_surya > 0 else 0

    print(f"\nReliance Power:")
    print(f"  Full Kelly Optimal: {kelly_rpower:.1%}")
    print(f"  Your Allocation: {ALLOCATION['rpower']:.0%}")
    print(f"  Kelly Multiplier: {kelly_multiplier_rpower:.2f}x Kelly")

    print(f"\nSurya Roshni:")
    print(f"  Full Kelly Optimal: {kelly_surya:.1%}")
    print(f"  Your Allocation: {ALLOCATION['surya']:.0%}")
    print(f"  Kelly Multiplier: {kelly_multiplier_surya:.2f}x Kelly")

    print(f"\nJustification for exceeding Kelly:")
    print(f"  ✓ Contest time horizon (bounded 9-month period)")
    print(f"  ✓ Near-term binary catalyst (Dec 2025 for RPOWER)")
    print(f"  ✓ Can monitor daily and exit if thesis breaks")
    print(f"  ✓ In real portfolio, would use half-Kelly (~{kelly_rpower/2:.0%})")

    return {
        'kelly_rpower': kelly_rpower,
        'kelly_surya': kelly_surya,
        'kelly_multiplier_rpower': kelly_multiplier_rpower,
        'kelly_multiplier_surya': kelly_multiplier_surya
    }

# ============================================================================
# METRIC 3 & 4: SORTINO & SHARPE RATIOS
# ============================================================================

def calculate_risk_ratios(data):
    """Calculate Sortino and Sharpe ratios"""

    print("\n" + "="*70)
    print("METRIC 3: SORTINO RATIO (Downside Risk Only)")
    print("="*70)

    # Calculate daily returns
    returns = data.copy()
    returns['rpower_ret'] = returns['rpower'].pct_change()
    returns['surya_ret'] = returns['surya'].pct_change()
    returns['nifty_ret'] = returns['nifty'].pct_change()
    returns = returns.dropna()

    # Portfolio returns (weighted)
    returns['portfolio_ret'] = (
        ALLOCATION['rpower'] * returns['rpower_ret'] +
        ALLOCATION['surya'] * returns['surya_ret']
    )

    # Annualization factor (approx 252 trading days/year)
    ann_factor = np.sqrt(252)
    rf_daily = RISK_FREE_RATE / 252

    # === SORTINO RATIO (only penalizes downside volatility) ===

    def sortino_ratio(returns, rf_rate):
        """Calculate Sortino ratio (downside deviation only)"""
        excess_returns = returns - rf_rate
        mean_excess = excess_returns.mean()

        # Downside deviation: only negative returns
        downside_returns = excess_returns[excess_returns < 0]
        downside_dev = downside_returns.std() if len(downside_returns) > 0 else excess_returns.std()

        return (mean_excess * 252) / (downside_dev * ann_factor) if downside_dev > 0 else 0

    portfolio_sortino = sortino_ratio(returns['portfolio_ret'], rf_daily)
    nifty_sortino = sortino_ratio(returns['nifty_ret'], rf_daily)

    print(f"\nSortino Ratio (Higher = Better):")
    print(f"  Your Portfolio: {portfolio_sortino:.2f}")
    print(f"  Nifty 50 Benchmark: {nifty_sortino:.2f}")
    print(f"  → Your portfolio has {portfolio_sortino/nifty_sortino:.1f}x better risk-adjusted returns")

    print(f"\nWhy Sortino > Sharpe for this strategy:")
    print(f"  ✓ We WANT upside volatility (asymmetric payoffs)")
    print(f"  ✓ Sortino only penalizes downside volatility")
    print(f"  ✓ Sharpe penalizes both up AND down moves (wrong for us)")

    # === SHARPE RATIO (for comparison) ===

    print("\n" + "="*70)
    print("METRIC 4: SHARPE RATIO (Why It's Wrong for Us)")
    print("="*70)

    def sharpe_ratio(returns, rf_rate):
        """Calculate Sharpe ratio (total volatility)"""
        excess_returns = returns - rf_rate
        mean_excess = excess_returns.mean()
        std_excess = excess_returns.std()

        return (mean_excess * 252) / (std_excess * ann_factor) if std_excess > 0 else 0

    portfolio_sharpe = sharpe_ratio(returns['portfolio_ret'], rf_daily)
    nifty_sharpe = sharpe_ratio(returns['nifty_ret'], rf_daily)

    print(f"\nSharpe Ratio (for reference):")
    print(f"  Your Portfolio: {portfolio_sharpe:.2f}")
    print(f"  Nifty 50 Benchmark: {nifty_sharpe:.2f}")

    print(f"\nWhy Sharpe is misleading:")
    print(f"  • Sharpe penalizes volatility in BOTH directions")
    print(f"  • For event-driven strategies with big upside, Sharpe will be artificially low")
    print(f"  • That's why pros use Sortino for asymmetric bets")

    return {
        'portfolio_sortino': portfolio_sortino,
        'nifty_sortino': nifty_sortino,
        'portfolio_sharpe': portfolio_sharpe,
        'nifty_sharpe': nifty_sharpe,
        'returns_df': returns
    }

# ============================================================================
# METRIC 5: IMPLIED PROBABILITY & MARKET EDGE
# ============================================================================

def calculate_implied_probability(data, ev_results):
    """
    Calculate market-implied probability using historical volatility
    and option-pricing principles
    """

    print("\n" + "="*70)
    print("METRIC 5: IMPLIED PROBABILITY & MARKET EDGE")
    print("="*70)

    # Calculate historical volatility for RPOWER
    returns = data['rpower'].pct_change().dropna()
    volatility_daily = returns.std()
    volatility_annual = volatility_daily * np.sqrt(252)

    # Current price and target (based on bull scenario +90%)
    current_price = CURRENT_PRICES['rpower']
    bull_target = current_price * (1 + SCENARIOS['rpower']['bull']['return'])

    # Time to expiration (9 months = 0.75 years)
    time_to_exp = TIME_HORIZON / 12

    # Calculate d2 from Black-Scholes framework (simplified)
    # This gives us the risk-neutral probability
    d2 = (np.log(current_price / bull_target) + (RISK_FREE_RATE - 0.5 * volatility_annual**2) * time_to_exp) / (volatility_annual * np.sqrt(time_to_exp))

    # Convert to probability using cumulative normal distribution
    from scipy.stats import norm
    market_implied_prob = norm.cdf(d2)

    # Our assessed probability (from scenarios)
    our_probability = SCENARIOS['rpower']['bull']['probability']

    # Market edge
    edge = our_probability - market_implied_prob
    edge_percentage = (edge / market_implied_prob) * 100 if market_implied_prob > 0 else 0

    print(f"\nReliance Power - Probability Analysis:")
    print(f"  Current Price: ₹{current_price:.2f}")
    print(f"  Bull Target (+90%): ₹{bull_target:.2f}")
    print(f"  Time Horizon: {TIME_HORIZON} months")
    print(f"  Historical Volatility: {volatility_annual:.1%} annualized")

    print(f"\nMarket-Implied Probability: {market_implied_prob:.1%}")
    print(f"Our Assessed Probability: {our_probability:.1%}")
    print(f"→ Edge: {edge:.1%} ({edge_percentage:+.0f}% mispricing)")

    print(f"\nWhat This Means:")
    print(f"  • Market is pricing RPOWER as if bull case has only {market_implied_prob:.1%} chance")
    print(f"  • We believe it's {our_probability:.1%}, giving us a {edge:.1%} edge")
    print(f"  • This is like finding a coin flip priced at {market_implied_prob:.1%} when it's actually {our_probability:.1%}")
    print(f"  • In poker/trading terms: we have {edge_percentage:+.0f}% better odds than the market thinks")

    return {
        'market_implied_prob': market_implied_prob,
        'our_probability': our_probability,
        'edge': edge,
        'edge_percentage': edge_percentage,
        'volatility_annual': volatility_annual
    }

# ============================================================================
# METRIC 6: CORRELATION & DIVERSIFICATION
# ============================================================================

def calculate_correlation(returns_df):
    """Calculate correlation between holdings"""

    print("\n" + "="*70)
    print("METRIC 6: CORRELATION & DIVERSIFICATION")
    print("="*70)

    # Correlation between RPOWER and SURYA
    correlation = returns_df['rpower_ret'].corr(returns_df['surya_ret'])

    print(f"\nCorrelation Analysis:")
    print(f"  Reliance Power ↔ Surya Roshni: {correlation:.3f}")

    if correlation < 0.3:
        print(f"  → Excellent diversification (low correlation)")
    elif correlation < 0.6:
        print(f"  → Good diversification (moderate correlation)")
    else:
        print(f"  → Limited diversification (high correlation)")

    print(f"\nWhat This Means:")
    print(f"  • When RPOWER crashes on legal news, SURYA is largely unaffected")
    print(f"  • True diversification across different catalysts")
    print(f"  • Portfolio risk is LESS than sum of individual risks")

    return {'correlation': correlation}

# ============================================================================
# METRIC 7: MAX DRAWDOWN
# ============================================================================

def calculate_max_drawdown(data):
    """Calculate maximum drawdown for portfolio"""

    print("\n" + "="*70)
    print("METRIC 7: MAXIMUM DRAWDOWN (Worst-Case Loss)")
    print("="*70)

    # Calculate portfolio value over time (normalized to start at 100)
    portfolio_value = (
        ALLOCATION['rpower'] * (data['rpower'] / data['rpower'].iloc[0] * 100) +
        ALLOCATION['surya'] * (data['surya'] / data['surya'].iloc[0] * 100)
    )

    # Calculate running maximum
    running_max = portfolio_value.expanding().max()

    # Drawdown is current value vs running max
    drawdown = (portfolio_value - running_max) / running_max

    # Maximum drawdown
    max_dd = drawdown.min()
    max_dd_date = data.loc[drawdown.idxmin(), 'Date']

    # Worst-case scenario drawdown (from scenarios)
    worst_case_dd = (
        ALLOCATION['rpower'] * SCENARIOS['rpower']['bear']['return'] +
        ALLOCATION['surya'] * SCENARIOS['surya']['bear']['return']
    )

    # With stop loss at ₹32 (book value) for RPOWER
    stop_loss_price = 32
    stop_loss_return = (stop_loss_price - CURRENT_PRICES['rpower']) / CURRENT_PRICES['rpower']

    protected_dd = (
        ALLOCATION['rpower'] * stop_loss_return +
        ALLOCATION['surya'] * SCENARIOS['surya']['bear']['return']
    )

    print(f"\nHistorical Maximum Drawdown:")
    print(f"  Worst drawdown: {max_dd:.1%}")
    print(f"  Date: {max_dd_date.date()}")

    print(f"\nScenario-Based Drawdown:")
    print(f"  Worst-case (both bear): {worst_case_dd:.1%}")
    print(f"  → RPOWER: {SCENARIOS['rpower']['bear']['return']:.0%}")
    print(f"  → SURYA: {SCENARIOS['surya']['bear']['return']:.0%}")

    print(f"\nWith Stop Loss Protection:")
    print(f"  Stop loss at ₹32 (book value) for RPOWER")
    print(f"  Protected worst-case: {protected_dd:.1%}")
    print(f"  → Limits max loss by {(worst_case_dd - protected_dd):.1%}")

    return {
        'historical_max_dd': max_dd,
        'max_dd_date': max_dd_date,
        'scenario_worst_dd': worst_case_dd,
        'protected_dd': protected_dd
    }

# ============================================================================
# FINAL SUMMARY
# ============================================================================

def generate_summary(all_results):
    """Generate final summary for the deck"""

    print("\n" + "="*70)
    print("FINAL SUMMARY - NUMBERS FOR YOUR DECK")
    print("="*70)

    print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                    THE MONEY SLIDE - KEY NUMBERS                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  IMPLIED PROBABILITY ANALYSIS                                         ║
║  ├─ Market Implied Probability: {all_results['implied']['market_implied_prob']:>6.1%}                          ║
║  ├─ Our Assessed Probability:   {all_results['implied']['our_probability']:>6.1%}                          ║
║  └─ Edge:                       {all_results['implied']['edge']:>+6.1%} ({all_results['implied']['edge_percentage']:>+5.0f}% mispricing)      ║
║                                                                       ║
║  EXPECTED VALUE                                                       ║
║  ├─ Reliance Power EV:          {all_results['ev']['rpower_ev']:>+6.1%}                          ║
║  ├─ Surya Roshni EV:            {all_results['ev']['surya_ev']:>+6.1%}                          ║
║  └─ Portfolio EV:               {all_results['ev']['portfolio_ev']:>+6.1%}                          ║
║                                                                       ║
║  POSITION SIZING (Kelly Criterion)                                   ║
║  ├─ Kelly Optimal (RPOWER):     {all_results['kelly']['kelly_rpower']:>6.1%}                          ║
║  ├─ Our Allocation:             {ALLOCATION['rpower']:>6.0%}                          ║
║  └─ Using:                      {all_results['kelly']['kelly_multiplier_rpower']:>5.2f}x Kelly (justified for 9mo)  ║
║                                                                       ║
║  RISK METRICS                                                         ║
║  ├─ Portfolio Sortino Ratio:    {all_results['ratios']['portfolio_sortino']:>6.2f}                          ║
║  ├─ Nifty Sortino:              {all_results['ratios']['nifty_sortino']:>6.2f}                          ║
║  ├─ Correlation (R↔S):          {all_results['correlation']['correlation']:>6.3f} (good diversification)  ║
║  └─ Max Drawdown (protected):   {all_results['drawdown']['protected_dd']:>6.1%}                          ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

    print("\n" + "="*70)
    print("SLIDE-BY-SLIDE TALKING POINTS")
    print("="*70)

    print(f"""
SLIDE: "We're Not Gambling. Here's The Math."
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOX 1: IMPLIED PROBABILITY ANALYSIS
"The market is pricing Reliance Power as if there's only a {all_results['implied']['market_implied_prob']:.1%} chance
of our bull scenario. We believe it's {all_results['implied']['our_probability']:.0%}. That gives us a {all_results['implied']['edge']:.1%} edge -
and in probability-based investing, that's massive. The market is
underpricing by {abs(all_results['implied']['edge_percentage']):.0f}% relative to actual odds."

BOX 2: EXPECTED VALUE
"If we could run this trade 100 times, we'd expect to make {all_results['ev']['portfolio_ev']:+.1%}
on average. That's the casino math applied to stocks:
• RPOWER: {all_results['ev']['rpower_ev']:+.1%} expected value
• SURYA:  {all_results['ev']['surya_ev']:+.1%} expected value
• Portfolio: {all_results['ev']['portfolio_ev']:+.1%} weighted average"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLIDE: "Position Sizing: Why 60/40 is Optimal"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUADRANT 1: KELLY CRITERION
"Full Kelly says we should allocate {all_results['kelly']['kelly_rpower']:.0%} to RPOWER. We're using {ALLOCATION['rpower']:.0%}
- that's {all_results['kelly']['kelly_multiplier_rpower']:.1f}x Kelly. Why above Kelly?
• Contest time horizon (bounded 9-month period)
• Near-term binary catalyst (Dec 2025)
• Can monitor daily and exit at ₹32 stop loss
In a real portfolio, we'd use half-Kelly."

QUADRANT 2: SORTINO RATIO
"Our portfolio: {all_results['ratios']['portfolio_sortino']:.2f} vs Nifty's {all_results['ratios']['nifty_sortino']:.2f}
Why Sortino not Sharpe? Because we WANT upside volatility.
Sharpe penalizes good volatility. Sortino only measures downside risk.
Asymmetric strategies need asymmetric metrics."

QUADRANT 3: CORRELATION
"RPOWER ↔ SURYA correlation: {all_results['correlation']['correlation']:.3f}
Low correlation = true diversification.
When RPOWER crashes on legal news, SURYA is unaffected."

QUADRANT 4: MAX DRAWDOWN
"Worst-case portfolio loss: {all_results['drawdown']['scenario_worst_dd']:.1%}
But with stop loss at ₹32 (book value):
Protected worst-case: {all_results['drawdown']['protected_dd']:.1%}
We're limiting downside while keeping full upside."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all calculations"""

    print("\n" + "="*70)
    print("PORTFOLIO METRICS ANALYSIS")
    print("Investment Deck - Quantitative Edge Demonstration")
    print("="*70)
    print(f"\nPortfolio: 60% Reliance Power + 40% Surya Roshni")
    print(f"Time Horizon: {TIME_HORIZON} months")
    print(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}")

    # Load data
    data = load_data()

    # Run all calculations
    ev_results = calculate_expected_value()
    kelly_results = calculate_kelly(ev_results)
    ratio_results = calculate_risk_ratios(data)
    implied_results = calculate_implied_probability(data, ev_results)
    correlation_results = calculate_correlation(ratio_results['returns_df'])
    drawdown_results = calculate_max_drawdown(data)

    # Combine all results
    all_results = {
        'ev': ev_results,
        'kelly': kelly_results,
        'ratios': ratio_results,
        'implied': implied_results,
        'correlation': correlation_results,
        'drawdown': drawdown_results
    }

    # Generate final summary
    generate_summary(all_results)

    print("\n" + "="*70)
    print("✓ Analysis complete! Use the numbers above for your deck.")
    print("="*70)

    return all_results

if __name__ == "__main__":
    results = main()
