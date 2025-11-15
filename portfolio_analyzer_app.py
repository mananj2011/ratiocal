"""
Portfolio Metrics Analyzer - Web Tool
======================================

A Streamlit web application for analyzing portfolio metrics including:
- Expected Value Analysis
- Kelly Criterion
- Sortino & Sharpe Ratios
- Implied Probability & Market Edge
- Correlation & Diversification
- Maximum Drawdown

Upload stock data from investing.com and get instant professional-grade analysis!
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Portfolio Metrics Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_investing_com_csv(uploaded_file):
    """Load and clean CSV from investing.com format"""
    df = pd.read_csv(uploaded_file)

    # Clean column names (remove BOM if present)
    df.columns = df.columns.str.replace('\ufeff', '').str.strip()

    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    # Clean price column (remove commas and convert to float)
    df['Price'] = df['Price'].astype(str).str.replace(',', '').astype(float)

    # Sort by date (oldest to newest)
    df = df.sort_values('Date').reset_index(drop=True)

    # Select only Date and Price
    df = df[['Date', 'Price']]

    return df

def calculate_ev(scenarios):
    """Calculate Expected Value from scenarios"""
    return sum(s['probability'] * s['return'] for s in scenarios.values())

def calculate_kelly(scenarios):
    """Calculate Kelly optimal position sizing"""
    # Separate winning and losing scenarios
    win_scenarios = {k: v for k, v in scenarios.items() if v['return'] > 0}
    loss_scenarios = {k: v for k, v in scenarios.items() if v['return'] < 0}

    win_prob = sum(s['probability'] for s in win_scenarios.values())
    loss_prob = sum(s['probability'] for s in loss_scenarios.values())

    if win_prob == 0:
        return 0

    # Expected win/loss amounts
    win_return = sum(s['probability'] * s['return'] for s in win_scenarios.values()) / win_prob

    if loss_prob > 0:
        loss_return = abs(sum(s['probability'] * s['return'] for s in loss_scenarios.values()) / loss_prob)
    else:
        loss_return = 0

    # Kelly formula
    if win_return > 0:
        kelly = (win_prob * win_return - loss_prob * loss_return) / win_return
    else:
        kelly = 0

    return max(0, min(1, kelly))

def calculate_sortino(returns, rf_rate):
    """Calculate Sortino ratio (downside deviation only)"""
    excess_returns = returns - rf_rate
    mean_excess = excess_returns.mean()

    # Downside deviation: only negative returns
    downside_returns = excess_returns[excess_returns < 0]
    downside_dev = downside_returns.std() if len(downside_returns) > 0 else excess_returns.std()

    ann_factor = np.sqrt(252)
    return (mean_excess * 252) / (downside_dev * ann_factor) if downside_dev > 0 else 0

def calculate_sharpe(returns, rf_rate):
    """Calculate Sharpe ratio (total volatility)"""
    excess_returns = returns - rf_rate
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std()

    ann_factor = np.sqrt(252)
    return (mean_excess * 252) / (std_excess * ann_factor) if std_excess > 0 else 0

def calculate_implied_probability(current_price, target_price, volatility_annual, time_to_exp, rf_rate):
    """Calculate market-implied probability using Black-Scholes framework"""
    d2 = (np.log(current_price / target_price) +
          (rf_rate - 0.5 * volatility_annual**2) * time_to_exp) / (volatility_annual * np.sqrt(time_to_exp))

    market_implied_prob = norm.cdf(d2)
    return market_implied_prob

def calculate_max_drawdown(prices):
    """Calculate maximum drawdown"""
    running_max = prices.expanding().max()
    drawdown = (prices - running_max) / running_max
    return drawdown.min()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Title and description
    st.title("📊 Portfolio Metrics Analyzer")
    st.markdown("""
    Upload your stock data from **investing.com** and get instant professional-grade portfolio analysis.

    **What you'll get:**
    - Expected Value Analysis (EV)
    - Kelly Criterion (optimal position sizing)
    - Sortino & Sharpe Ratios
    - Implied Probability & Market Edge
    - Correlation & Diversification metrics
    - Maximum Drawdown analysis
    """)

    st.markdown("---")

    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")

    # Risk-free rate
    rf_rate = st.sidebar.number_input(
        "Risk-Free Rate (Annual %)",
        min_value=0.0,
        max_value=20.0,
        value=7.0,
        step=0.1,
        help="Approximate T-bill or government bond rate"
    ) / 100

    # Time horizon
    time_horizon = st.sidebar.number_input(
        "Investment Horizon (Months)",
        min_value=1,
        max_value=60,
        value=9,
        step=1
    )

    st.sidebar.markdown("---")

    # Number of stocks in portfolio
    num_stocks = st.sidebar.number_input(
        "Number of Stocks in Portfolio",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

    # ========================================================================
    # FILE UPLOADS
    # ========================================================================

    st.header("1️⃣ Upload Stock Data")
    st.markdown("Upload CSV files from investing.com (same format as RPOWER/SURYA/Nifty)")

    # Create columns for stock uploads
    stock_data = {}
    stock_names = []

    cols = st.columns(min(num_stocks, 3))

    for i in range(num_stocks):
        col_idx = i % 3
        with cols[col_idx]:
            stock_name = st.text_input(f"Stock {i+1} Name", value=f"Stock_{i+1}", key=f"name_{i}")
            stock_names.append(stock_name)

            uploaded_file = st.file_uploader(
                f"Upload {stock_name} CSV",
                type=['csv'],
                key=f"upload_{i}"
            )

            if uploaded_file:
                try:
                    stock_data[stock_name] = load_investing_com_csv(uploaded_file)
                    st.success(f"✓ Loaded {len(stock_data[stock_name])} days of data")
                except Exception as e:
                    st.error(f"Error loading file: {e}")

    # Benchmark upload
    st.markdown("---")
    st.subheader("Benchmark Index (e.g., Nifty 50)")

    benchmark_file = st.file_uploader(
        "Upload Benchmark CSV",
        type=['csv'],
        key="benchmark"
    )

    benchmark_data = None
    if benchmark_file:
        try:
            benchmark_data = load_investing_com_csv(benchmark_file)
            st.success(f"✓ Loaded {len(benchmark_data)} days of benchmark data")
        except Exception as e:
            st.error(f"Error loading benchmark: {e}")

    # ========================================================================
    # PORTFOLIO ALLOCATION
    # ========================================================================

    if stock_data:
        st.markdown("---")
        st.header("2️⃣ Portfolio Allocation")

        allocations = {}
        allocation_cols = st.columns(min(num_stocks, 4))

        for i, stock_name in enumerate(stock_names):
            if stock_name in stock_data:
                col_idx = i % 4
                with allocation_cols[col_idx]:
                    allocations[stock_name] = st.number_input(
                        f"{stock_name} %",
                        min_value=0.0,
                        max_value=100.0,
                        value=100.0 / len(stock_data),
                        step=1.0,
                        key=f"alloc_{i}"
                    ) / 100

        # Check if allocations sum to 100%
        total_allocation = sum(allocations.values()) * 100
        if abs(total_allocation - 100) > 0.1:
            st.warning(f"⚠️ Allocations sum to {total_allocation:.1f}% (should be 100%)")
        else:
            st.success(f"✓ Allocations sum to {total_allocation:.1f}%")

        # ====================================================================
        # CURRENT PRICES
        # ====================================================================

        st.markdown("---")
        st.header("3️⃣ Current Prices")

        current_prices = {}
        price_cols = st.columns(min(num_stocks, 4))

        for i, stock_name in enumerate(stock_names):
            if stock_name in stock_data:
                col_idx = i % 4
                latest_price = stock_data[stock_name]['Price'].iloc[-1]

                with price_cols[col_idx]:
                    current_prices[stock_name] = st.number_input(
                        f"{stock_name} Current Price",
                        min_value=0.0,
                        value=float(latest_price),
                        step=0.01,
                        key=f"price_{i}"
                    )

        # ====================================================================
        # SCENARIO ANALYSIS
        # ====================================================================

        st.markdown("---")
        st.header("4️⃣ Scenario Analysis")
        st.markdown("Define probability-weighted scenarios for each stock")

        scenarios = {}

        for stock_name in stock_names:
            if stock_name in stock_data:
                with st.expander(f"📈 {stock_name} Scenarios", expanded=False):
                    num_scenarios = st.number_input(
                        f"Number of scenarios for {stock_name}",
                        min_value=1,
                        max_value=10,
                        value=3,
                        key=f"num_scen_{stock_name}"
                    )

                    scenarios[stock_name] = {}

                    cols = st.columns(3)

                    for j in range(num_scenarios):
                        with cols[j % 3]:
                            scenario_name = st.text_input(
                                f"Scenario {j+1} Name",
                                value=f"Scenario_{j+1}",
                                key=f"scen_name_{stock_name}_{j}"
                            )

                            probability = st.number_input(
                                f"Probability %",
                                min_value=0.0,
                                max_value=100.0,
                                value=100.0 / num_scenarios,
                                step=1.0,
                                key=f"prob_{stock_name}_{j}"
                            ) / 100

                            return_pct = st.number_input(
                                f"Return %",
                                min_value=-100.0,
                                max_value=1000.0,
                                value=0.0,
                                step=1.0,
                                key=f"ret_{stock_name}_{j}"
                            ) / 100

                            scenarios[stock_name][scenario_name] = {
                                'probability': probability,
                                'return': return_pct
                            }

                    # Check if probabilities sum to 100%
                    total_prob = sum(s['probability'] for s in scenarios[stock_name].values()) * 100
                    if abs(total_prob - 100) > 0.1:
                        st.warning(f"⚠️ Probabilities sum to {total_prob:.1f}% (should be 100%)")
                    else:
                        st.success(f"✓ Probabilities sum to {total_prob:.1f}%")

        # ====================================================================
        # CALCULATE BUTTON
        # ====================================================================

        st.markdown("---")

        if st.button("🚀 Calculate All Metrics", type="primary", use_container_width=True):

            # Check if we have all required data
            if not stock_data:
                st.error("Please upload at least one stock CSV file")
                return

            if not benchmark_data:
                st.warning("No benchmark data uploaded. Some metrics will be limited.")

            # ================================================================
            # MERGE DATA
            # ================================================================

            with st.spinner("Processing data..."):
                # Merge all stock data
                merged_data = None

                for stock_name, df in stock_data.items():
                    df_copy = df.copy()
                    df_copy = df_copy.rename(columns={'Price': stock_name})

                    if merged_data is None:
                        merged_data = df_copy
                    else:
                        merged_data = merged_data.merge(df_copy, on='Date', how='inner')

                # Add benchmark if available
                if benchmark_data is not None:
                    benchmark_copy = benchmark_data.copy()
                    benchmark_copy = benchmark_copy.rename(columns={'Price': 'Benchmark'})
                    merged_data = merged_data.merge(benchmark_copy, on='Date', how='inner')

                st.success(f"✓ Merged data: {len(merged_data)} trading days")
                st.info(f"📅 Date range: {merged_data['Date'].min().date()} to {merged_data['Date'].max().date()}")

            # ================================================================
            # CALCULATE METRICS
            # ================================================================

            st.markdown("---")
            st.header("📊 Results")

            # Calculate returns
            returns_df = merged_data.copy()
            for stock_name in stock_names:
                if stock_name in stock_data:
                    returns_df[f'{stock_name}_ret'] = returns_df[stock_name].pct_change()

            if benchmark_data is not None:
                returns_df['Benchmark_ret'] = returns_df['Benchmark'].pct_change()

            returns_df = returns_df.dropna()

            # Portfolio returns
            returns_df['Portfolio_ret'] = sum(
                allocations.get(stock_name, 0) * returns_df[f'{stock_name}_ret']
                for stock_name in stock_names if stock_name in stock_data
            )

            rf_daily = rf_rate / 252

            # ============================================================
            # METRIC 1: EXPECTED VALUE
            # ============================================================

            st.subheader("1️⃣ Expected Value Analysis")

            ev_results = {}

            cols = st.columns(min(len(stock_data) + 1, 4))

            for i, stock_name in enumerate(stock_names):
                if stock_name in stock_data and stock_name in scenarios:
                    ev = calculate_ev(scenarios[stock_name])
                    ev_results[stock_name] = ev

                    with cols[i % 4]:
                        st.metric(
                            label=f"{stock_name} EV",
                            value=f"{ev*100:+.1f}%"
                        )

            # Portfolio EV
            portfolio_ev = sum(
                allocations.get(stock_name, 0) * ev_results.get(stock_name, 0)
                for stock_name in stock_names
            )

            with cols[len(ev_results) % 4]:
                st.metric(
                    label="Portfolio EV",
                    value=f"{portfolio_ev*100:+.1f}%",
                    delta="Weighted Average"
                )

            # ============================================================
            # METRIC 2: KELLY CRITERION
            # ============================================================

            st.markdown("---")
            st.subheader("2️⃣ Kelly Criterion (Optimal Position Sizing)")

            kelly_results = {}

            kelly_data = []

            for stock_name in stock_names:
                if stock_name in stock_data and stock_name in scenarios:
                    kelly = calculate_kelly(scenarios[stock_name])
                    kelly_results[stock_name] = kelly

                    actual_allocation = allocations.get(stock_name, 0)
                    kelly_multiplier = actual_allocation / kelly if kelly > 0 else 0

                    kelly_data.append({
                        'Stock': stock_name,
                        'Kelly Optimal': f"{kelly*100:.1f}%",
                        'Your Allocation': f"{actual_allocation*100:.1f}%",
                        'Kelly Multiplier': f"{kelly_multiplier:.2f}x"
                    })

            kelly_df = pd.DataFrame(kelly_data)
            st.dataframe(kelly_df, use_container_width=True, hide_index=True)

            # ============================================================
            # METRIC 3 & 4: SORTINO & SHARPE
            # ============================================================

            st.markdown("---")
            st.subheader("3️⃣ Sortino & Sharpe Ratios")

            portfolio_sortino = calculate_sortino(returns_df['Portfolio_ret'], rf_daily)
            portfolio_sharpe = calculate_sharpe(returns_df['Portfolio_ret'], rf_daily)

            if benchmark_data is not None:
                benchmark_sortino = calculate_sortino(returns_df['Benchmark_ret'], rf_daily)
                benchmark_sharpe = calculate_sharpe(returns_df['Benchmark_ret'], rf_daily)
            else:
                benchmark_sortino = None
                benchmark_sharpe = None

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Portfolio Sortino", f"{portfolio_sortino:.2f}")

            with col2:
                if benchmark_sortino:
                    st.metric("Benchmark Sortino", f"{benchmark_sortino:.2f}")
                else:
                    st.metric("Benchmark Sortino", "N/A")

            with col3:
                st.metric("Portfolio Sharpe", f"{portfolio_sharpe:.2f}")

            with col4:
                if benchmark_sharpe:
                    st.metric("Benchmark Sharpe", f"{benchmark_sharpe:.2f}")
                else:
                    st.metric("Benchmark Sharpe", "N/A")

            if benchmark_sortino:
                advantage = portfolio_sortino / benchmark_sortino if benchmark_sortino > 0 else 0
                st.info(f"📈 Your portfolio has **{advantage:.2f}x** better risk-adjusted returns (Sortino)")

            st.markdown("""
            **Why Sortino > Sharpe for asymmetric strategies:**
            - Sortino only penalizes downside volatility
            - Sharpe penalizes both up and down moves
            - For event-driven strategies with big upside, use Sortino
            """)

            # ============================================================
            # METRIC 5: IMPLIED PROBABILITY (for first stock)
            # ============================================================

            st.markdown("---")
            st.subheader("4️⃣ Implied Probability & Market Edge")

            # Calculate for the first stock with bull scenario
            first_stock = stock_names[0] if stock_names and stock_names[0] in stock_data else None

            if first_stock and first_stock in scenarios:
                # Find bull scenario (highest return)
                bull_scenario = max(scenarios[first_stock].items(), key=lambda x: x[1]['return'])

                current_price = current_prices.get(first_stock, merged_data[first_stock].iloc[-1])
                bull_target = current_price * (1 + bull_scenario[1]['return'])

                # Calculate historical volatility
                stock_returns = merged_data[first_stock].pct_change().dropna()
                volatility_daily = stock_returns.std()
                volatility_annual = volatility_daily * np.sqrt(252)

                time_to_exp = time_horizon / 12

                market_implied_prob = calculate_implied_probability(
                    current_price, bull_target, volatility_annual, time_to_exp, rf_rate
                )

                our_probability = bull_scenario[1]['probability']
                edge = our_probability - market_implied_prob
                edge_pct = (edge / market_implied_prob * 100) if market_implied_prob > 0 else 0

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Market Implied Probability", f"{market_implied_prob*100:.1f}%")

                with col2:
                    st.metric("Your Assessed Probability", f"{our_probability*100:.1f}%")

                with col3:
                    st.metric("Edge", f"{edge*100:+.1f}%", delta=f"{edge_pct:+.0f}% mispricing")

                st.info(f"""
                📊 **{first_stock} Analysis:**
                - Current Price: ₹{current_price:.2f}
                - Bull Target: ₹{bull_target:.2f}
                - Historical Volatility: {volatility_annual*100:.1f}% annualized
                - Market thinks bull scenario has {market_implied_prob*100:.1f}% chance
                - You think it's {our_probability*100:.0f}%, giving you a **{edge*100:.1f}%** edge
                """)

            # ============================================================
            # METRIC 6: CORRELATION
            # ============================================================

            st.markdown("---")
            st.subheader("5️⃣ Correlation & Diversification")

            if len(stock_data) >= 2:
                # Create correlation matrix
                corr_cols = [f'{s}_ret' for s in stock_names if s in stock_data]
                corr_matrix = returns_df[corr_cols].corr()

                # Rename columns/index for display
                corr_matrix.columns = [s for s in stock_names if s in stock_data]
                corr_matrix.index = [s for s in stock_names if s in stock_data]

                # Display heatmap
                fig = px.imshow(
                    corr_matrix,
                    labels=dict(color="Correlation"),
                    x=corr_matrix.columns,
                    y=corr_matrix.index,
                    color_continuous_scale='RdYlGn_r',
                    zmin=-1,
                    zmax=1,
                    text_auto='.3f'
                )
                fig.update_layout(title="Correlation Matrix")
                st.plotly_chart(fig, use_container_width=True)

                # Interpretation
                avg_corr = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()

                if avg_corr < 0.3:
                    st.success(f"✓ Excellent diversification (average correlation: {avg_corr:.3f})")
                elif avg_corr < 0.6:
                    st.info(f"✓ Good diversification (average correlation: {avg_corr:.3f})")
                else:
                    st.warning(f"⚠️ Limited diversification (average correlation: {avg_corr:.3f})")

            # ============================================================
            # METRIC 7: MAX DRAWDOWN
            # ============================================================

            st.markdown("---")
            st.subheader("6️⃣ Maximum Drawdown")

            # Calculate portfolio value over time
            portfolio_value = sum(
                allocations.get(stock_name, 0) * (merged_data[stock_name] / merged_data[stock_name].iloc[0] * 100)
                for stock_name in stock_names if stock_name in stock_data
            )

            historical_max_dd = calculate_max_drawdown(portfolio_value)

            # Scenario-based worst case
            worst_case_dd = sum(
                allocations.get(stock_name, 0) * min(s['return'] for s in scenarios.get(stock_name, {}).values())
                for stock_name in stock_names if stock_name in scenarios
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Historical Max Drawdown", f"{historical_max_dd*100:.1f}%")

            with col2:
                st.metric("Scenario Worst-Case", f"{worst_case_dd*100:.1f}%")

            # Drawdown chart
            running_max = portfolio_value.expanding().max()
            drawdown = (portfolio_value - running_max) / running_max * 100

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=merged_data['Date'],
                y=drawdown,
                fill='tozeroy',
                name='Drawdown %',
                line=dict(color='red')
            ))
            fig.update_layout(
                title="Portfolio Drawdown Over Time",
                xaxis_title="Date",
                yaxis_title="Drawdown %",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

            # ============================================================
            # PORTFOLIO PERFORMANCE CHART
            # ============================================================

            st.markdown("---")
            st.subheader("📈 Portfolio Performance")

            # Normalize to 100
            fig = go.Figure()

            for stock_name in stock_names:
                if stock_name in stock_data:
                    normalized = merged_data[stock_name] / merged_data[stock_name].iloc[0] * 100
                    fig.add_trace(go.Scatter(
                        x=merged_data['Date'],
                        y=normalized,
                        name=stock_name,
                        mode='lines'
                    ))

            fig.add_trace(go.Scatter(
                x=merged_data['Date'],
                y=portfolio_value,
                name='Portfolio (Weighted)',
                mode='lines',
                line=dict(width=3, color='black')
            ))

            if benchmark_data is not None:
                benchmark_normalized = merged_data['Benchmark'] / merged_data['Benchmark'].iloc[0] * 100
                fig.add_trace(go.Scatter(
                    x=merged_data['Date'],
                    y=benchmark_normalized,
                    name='Benchmark',
                    mode='lines',
                    line=dict(dash='dash', color='gray')
                ))

            fig.update_layout(
                title="Normalized Performance (Base = 100)",
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # ============================================================
            # SUMMARY TABLE
            # ============================================================

            st.markdown("---")
            st.subheader("📋 Summary Table")

            summary_data = {
                'Metric': [
                    'Portfolio Expected Value',
                    'Portfolio Sortino Ratio',
                    'Portfolio Sharpe Ratio',
                    'Historical Max Drawdown',
                    'Scenario Worst-Case Drawdown',
                    'Average Correlation',
                ],
                'Value': [
                    f"{portfolio_ev*100:+.1f}%",
                    f"{portfolio_sortino:.2f}",
                    f"{portfolio_sharpe:.2f}",
                    f"{historical_max_dd*100:.1f}%",
                    f"{worst_case_dd*100:.1f}%",
                    f"{avg_corr:.3f}" if len(stock_data) >= 2 else "N/A",
                ]
            }

            if benchmark_data is not None:
                summary_data['Benchmark'] = [
                    "N/A",
                    f"{benchmark_sortino:.2f}",
                    f"{benchmark_sharpe:.2f}",
                    "N/A",
                    "N/A",
                    "N/A",
                ]

            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            # ============================================================
            # EXPORT RESULTS
            # ============================================================

            st.markdown("---")
            st.subheader("💾 Export Results")

            # Create downloadable report
            report = f"""
# Portfolio Metrics Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Portfolio Configuration
- Time Horizon: {time_horizon} months
- Risk-Free Rate: {rf_rate*100:.1f}%

### Allocation
"""
            for stock_name, alloc in allocations.items():
                report += f"- {stock_name}: {alloc*100:.1f}%\n"

            report += f"""

## Key Metrics

### Expected Value
- Portfolio EV: {portfolio_ev*100:+.1f}%
"""
            for stock_name, ev in ev_results.items():
                report += f"- {stock_name} EV: {ev*100:+.1f}%\n"

            report += f"""

### Risk Metrics
- Portfolio Sortino Ratio: {portfolio_sortino:.2f}
- Portfolio Sharpe Ratio: {portfolio_sharpe:.2f}
"""
            if benchmark_data is not None:
                report += f"- Benchmark Sortino: {benchmark_sortino:.2f}\n"
                report += f"- Benchmark Sharpe: {benchmark_sharpe:.2f}\n"

            report += f"""

### Drawdown Analysis
- Historical Max Drawdown: {historical_max_dd*100:.1f}%
- Scenario Worst-Case: {worst_case_dd*100:.1f}%
"""

            if len(stock_data) >= 2:
                report += f"\n### Diversification\n- Average Correlation: {avg_corr:.3f}\n"

            # Download button
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=report,
                file_name=f"portfolio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
