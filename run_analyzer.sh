#!/bin/bash

# Portfolio Metrics Analyzer - Quick Start Script

echo "🚀 Starting Portfolio Metrics Analyzer..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "📦 Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "🌐 Opening web app at http://localhost:8501"
echo ""
echo "📖 Quick Guide:"
echo "  1. Upload stock CSVs from investing.com"
echo "  2. Set allocations (must sum to 100%)"
echo "  3. Define scenarios with probabilities"
echo "  4. Click 'Calculate All Metrics'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
streamlit run portfolio_analyzer_app.py
