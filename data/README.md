# Historical Data Files

Please add the following CSV files to this directory:

## Required Files

1. **reliance_power.csv** - 1 year daily price data
2. **surya_roshni.csv** - 1 year daily price data
3. **nifty50.csv** - 1 year daily price data

## Expected CSV Format

Each file should have at minimum these columns:
```
Date,Close
2024-01-15,45.30
2024-01-16,46.20
...
```

- **Date**: Any standard date format (YYYY-MM-DD preferred)
- **Close**: Closing price

Additional columns (Open, High, Low, Volume) are fine but not required.

## How to Add Files

### Option 1: Using Git Command Line
```bash
# Copy your CSV files to this directory, then:
git add data/*.csv
git commit -m "Add historical price data for analysis"
git push
```

### Option 2: Using GitHub Web Interface
1. Go to your repository on GitHub
2. Navigate to the `data` folder
3. Click "Add file" → "Upload files"
4. Drag and drop your 3 CSV files
5. Commit the changes

### Option 3: Using Git GUI/Desktop
1. Copy the 3 CSV files into this `data/` folder on your computer
2. Use your Git GUI to stage and commit the files
3. Push to the repository

Once the files are added, the analysis script will automatically read them.
