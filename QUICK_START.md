# Quick Start Guide 🚀

Get professional portfolio metrics in 5 minutes!

## Step 1: Install & Run

```bash
# Option 1: Use the quick start script
./run_analyzer.sh

# Option 2: Manual start
pip install -r requirements.txt
streamlit run portfolio_analyzer_app.py
```

The app will open at **http://localhost:8501**

## Step 2: Get Your Data from Investing.com

1. Go to [investing.com](https://www.investing.com)
2. Search for your stock (e.g., "Reliance Power")
3. Click **"Historical Data"** tab
4. Select timeframe (e.g., **1 year**)
5. Click **"Download"** button
6. Save the CSV file

**Repeat for:**
- Each stock in your portfolio
- Your benchmark index (e.g., Nifty 50)

## Step 3: Upload Files

In the web app:
1. Enter number of stocks (e.g., 2)
2. Name each stock
3. Upload the CSV for each stock
4. Upload benchmark CSV

You'll see: ✓ Loaded XXX days of data

## Step 4: Configure Portfolio

### Set Allocations
- Stock 1: 60%
- Stock 2: 40%
- **Must sum to 100%** ✓

### Enter Current Prices
The app pre-fills with latest price from CSV, but you can update.

## Step 5: Define Scenarios

For each stock, create scenarios with:
- Scenario name (e.g., "Bull", "Base", "Bear")
- Probability % (must sum to 100%)
- Expected return %

**Example for Reliance Power:**

| Scenario | Probability | Return |
|----------|-------------|--------|
| Bull | 30% | +90% |
| Mixed | 50% | +15% |
| Bear | 20% | -40% |

**Example for Surya Roshni:**

| Scenario | Probability | Return |
|----------|-------------|--------|
| Base | 60% | +27% |
| Bull | 25% | +64% |
| Bear | 15% | -18% |

## Step 6: Calculate!

Click **"🚀 Calculate All Metrics"**

You'll get:
- ✅ Expected Value
- ✅ Kelly Criterion
- ✅ Sortino & Sharpe Ratios
- ✅ Implied Probability & Edge
- ✅ Correlation Matrix
- ✅ Maximum Drawdown
- ✅ Performance Charts
- ✅ Downloadable Report

## Common Scenarios to Try

### Conservative Strategy
- Base case: 70% probability, +15% return
- Bull case: 20% probability, +40% return
- Bear case: 10% probability, -10% return

### Aggressive Event-Driven
- Bull case: 35% probability, +120% return
- Mixed case: 45% probability, +25% return
- Bear case: 20% probability, -50% return

### Balanced Growth
- Base case: 60% probability, +20% return
- Bull case: 25% probability, +50% return
- Bear case: 15% probability, -15% return

## Understanding Your Results

### Expected Value (EV)
**Good:** +15% to +30%
**Excellent:** +30% or higher

*This is your average return if you ran the trade 100 times*

### Sortino Ratio
**Good:** 0.5 - 1.0
**Excellent:** 1.0 or higher

*Higher = better risk-adjusted returns*

### Kelly Multiplier
**Conservative:** 0.25x - 0.5x Kelly (half-Kelly)
**Optimal:** 0.8x - 1.2x Kelly
**Aggressive:** 1.2x - 2.0x Kelly

*1.0x = mathematically optimal for long-term*

### Market Edge
**Good:** +5% to +10%
**Excellent:** +10% or higher

*How much better are your odds vs what market thinks*

### Correlation
**Excellent:** 0.0 - 0.3 (low correlation)
**Good:** 0.3 - 0.6 (moderate)
**Poor:** 0.6 - 1.0 (high correlation)

*Lower = better diversification*

## Troubleshooting

### "Allocations don't sum to 100%"
Make sure your percentages add up to exactly 100.0%

### "Probabilities don't sum to 100%"
Check each stock's scenarios - probabilities must total 100%

### "No data after merging"
Your CSV files might have different date ranges. Use files with overlapping dates.

### "File upload error"
Make sure your CSV has these columns: `Date`, `Price`

## Pro Tips

### Tip 1: Use 1 Year of Data
1 year gives you ~250 trading days - enough for good statistics.

### Tip 2: Be Realistic with Scenarios
Don't create bull scenarios with 5% probability and 1000% returns just to game the EV.
Use realistic probabilities based on your research.

### Tip 3: Compare to Benchmark
Always upload a benchmark (Nifty 50) to show how your portfolio compares.

### Tip 4: Check Correlation
If correlation is >0.7, you don't have true diversification.

### Tip 5: Download the Report
Use the "Download Report" button to save your analysis as a Markdown file.

## Example Output

```
Portfolio Expected Value: +27.7%
Portfolio Sortino Ratio: 0.75
Nifty Sortino: 0.51
→ 1.5x better risk-adjusted returns

Market Implied Probability: 7.4%
Your Assessed Probability: 30.0%
→ Edge: +22.6% (306% mispricing)

Kelly Optimal: 61%
Your Allocation: 60%
→ 0.98x Kelly (optimal!)

Max Drawdown: -20.7% (with stop loss)
```

## Next Steps

1. **Take screenshots** of your results
2. **Download the report** (Markdown file)
3. **Copy numbers** into your investment deck
4. **Use the talking points** from the Summary section

## Need Help?

- Check `README.md` for detailed documentation
- Review `DECK_NUMBERS.md` for example analysis
- Run `portfolio_metrics_analysis.py` for a worked example

---

**Happy analyzing! 📊**
