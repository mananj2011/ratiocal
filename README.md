# Portfolio Metrics Analyzer 📊

A professional-grade web tool for analyzing portfolio metrics using historical stock data from investing.com.

## 🎯 What It Does

Calculate **all the metrics** that make you look smart in investment presentations:

1. **Expected Value Analysis** - Probability-weighted scenario returns
2. **Kelly Criterion** - Optimal position sizing (like pros)
3. **Sortino Ratio** - Risk-adjusted returns (better than Sharpe for asymmetric strategies)
4. **Sharpe Ratio** - For comparison (to show why it's wrong!)
5. **Implied Probability** - Quantify market mispricing
6. **Correlation Matrix** - Diversification analysis
7. **Maximum Drawdown** - Worst-case scenario analysis

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run portfolio_analyzer_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Data Format

The tool accepts CSV files from **investing.com** with this format:

```csv
Date,Price,Open,High,Low,Vol.,Change %
11/14/2025,41.33,41.12,41.77,41.00,20.73M,0.17%
11/13/2025,41.26,41.88,42.59,41.00,42.50M,-1.08%
...
```

**Required columns:** `Date`, `Price`

**How to get data from investing.com:**
1. Go to investing.com
2. Search for your stock (e.g., "Reliance Power")
3. Click "Historical Data"
4. Select timeframe (e.g., 1 year)
5. Click "Download" to get CSV

## 📖 How to Use

### Step 1: Upload Data
- Upload CSV files for each stock in your portfolio
- Upload benchmark index (e.g., Nifty 50) - optional but recommended

### Step 2: Configure Portfolio
- Set allocation percentages (must sum to 100%)
- Enter current prices for each stock

### Step 3: Define Scenarios
For each stock, create probability-weighted scenarios:

**Example (Reliance Power):**
- Bull (30% probability): +90% return
- Mixed (50% probability): +15% return
- Bear (20% probability): -40% return

### Step 4: Calculate
Click "Calculate All Metrics" and get instant results!

## 🎓 Understanding the Metrics

### Expected Value (EV)
> "If you ran this trade 100 times, what would you make on average?"

**Example:**
- EV = (30% × 90%) + (50% × 15%) + (20% × -40%) = +26.5%

### Kelly Criterion
> "What's the mathematically optimal position size?"

**Why it matters:** Shows you size positions like a professional gambler/trader, not emotionally.

**Example:**
- Kelly says: 61% allocation
- You're using: 60%
- You're at 0.98x Kelly (nearly optimal!)

### Sortino Ratio
> "Risk-adjusted returns, but ONLY counting downside risk"

**Why use Sortino instead of Sharpe?**
- ✓ We WANT upside volatility (big gains)
- ✓ Sortino only penalizes bad volatility (losses)
- ✓ Sharpe penalizes both up and down (wrong for event-driven strategies)

**Example:**
- Your portfolio: 0.75
- Nifty benchmark: 0.51
- You're 1.5x better on risk-adjusted returns

### Implied Probability
> "What does the market think the probability is? Are they wrong?"

**Example:**
- Market thinks: 7.4% chance of bull scenario
- You think: 30% chance
- Edge: +22.6% (306% mispricing!)

This is your **quantifiable edge** - like finding a coin flip priced at 7% when it's actually 30%.

### Correlation
> "When one stock crashes, does the other crash too?"

**Low correlation (0.0 - 0.3):** Excellent diversification ✓
**Moderate (0.3 - 0.6):** Good diversification
**High (0.6 - 1.0):** Limited diversification

### Maximum Drawdown
> "What's the worst loss you could experience?"

**Example:**
- Historical worst: -35.8%
- Scenario worst-case: -31.2%
- With stop-loss protection: -20.7%

## 💡 Pro Tips

### 1. Use Sortino, Not Sharpe
"Most investors use Sharpe Ratio. We use Sortino. Why? Because we WANT upside volatility. Sharpe penalizes us for making money too fast."

### 2. Show Your Edge
"The market is pricing this at 7% probability. We think it's 30%. That's a 23% edge."

### 3. Size Positions Mathematically
"Kelly Criterion says 61%. We're using 60%. That's optimal for this time horizon."

### 4. Quantify Diversification
"Don't just say 'we're diversified' - show the correlation: 0.352 means when one crashes, the other doesn't."

## 📊 Example Use Case

**Portfolio:** 60% Reliance Power + 40% Surya Roshni

**Scenario (RPOWER):**
- Bull (30%): +90%
- Mixed (50%): +15%
- Bear (20%): -40%

**Results:**
- Expected Value: +27.7%
- Sortino Ratio: 0.75 (vs Nifty 0.51)
- Market Edge: +22.6%
- Kelly Optimal: 60% (you're at 1.0x Kelly)
- Max Drawdown: -20.7% (with stop loss)

**What to say:**
"We have a quantifiable 23% edge over the market, with an expected value of +28%. Our position sizing is mathematically optimal via Kelly Criterion, and our risk-adjusted returns are 1.5x better than Nifty using Sortino Ratio."

## 🎯 What Makes You Look Smart

1. **You think in probabilities, not certainties**
   - "30% chance of 90% return" vs "it's going to moon!"

2. **You size positions mathematically**
   - "Kelly Criterion says 61%" vs "I put 60% because I like it"

3. **You use the RIGHT metrics**
   - "Sortino not Sharpe for asymmetric bets" - instantly separates you from amateurs

4. **You quantify your edge**
   - "Market implies 7%, we think 30%, that's a 23% edge"

5. **You understand diversification**
   - "0.352 correlation means true diversification" vs "we have two stocks"

## 📁 Files in This Project

- `portfolio_analyzer_app.py` - Main Streamlit web application
- `portfolio_metrics_analysis.py` - Original analysis script for RPOWER/SURYA
- `DECK_NUMBERS.md` - Summary of metrics for investment deck
- `requirements.txt` - Python dependencies
- `data/` - Historical price data from investing.com
- `README.md` - This file

## 🛠️ Technical Details

**Built with:**
- Python 3.11+
- Streamlit (web framework)
- Pandas (data processing)
- NumPy (numerical calculations)
- SciPy (statistical functions)
- Plotly (interactive charts)

**Calculations:**
- Expected Value: Probability-weighted scenario returns
- Kelly Criterion: Optimal bet sizing formula
- Sortino Ratio: (Mean excess return) / (Downside deviation)
- Sharpe Ratio: (Mean excess return) / (Total deviation)
- Implied Probability: Black-Scholes d2 calculation
- Correlation: Pearson correlation coefficient
- Max Drawdown: Maximum peak-to-trough decline

## 🤝 Contributing

This is a personal project, but feel free to fork and customize!

## 📄 License

MIT License - Free to use for personal or commercial projects

## 🙋 Support

For issues or questions:
1. Check the FAQ in this README
2. Review the example analysis in `DECK_NUMBERS.md`
3. Run `streamlit run portfolio_analyzer_app.py` and experiment!

---

**Made for investors who think like poker players, size positions like Kelly, and use Sortino instead of Sharpe.** 🎯
