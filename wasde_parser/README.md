# WASDE Wheat: Quantifying Market Volatility Around Major Agricultural Reports

This tool automates the analysis of USDA WASDE (World Agricultural Supply and Demand Estimates) reports. It parses unstructured government data to extract key "Ending Stocks" metrics and correlates them with CBOT Wheat Futures (ZW=F) price action to visualize market stress and volatility regimes.


## Project Purpose

For grain traders, the monthly WASDE report is a high-volatility event. A surprise in Ending Stocks (the amount of crop left over at the end of the year) can cause massive price dislocations.

This project solves three problems:

1. **Parsing**: Automates the extraction of specific data points (US & World Ending Stocks) from messy Excel/CSV government reports.

2. **Context**: Calculates the Month-on-Month (MoM) change to identify bullish/bearish surprises.

3. **Risk Analysis**: Visualizes the "Stress" (Absolute Price Returns) in the days surrounding the report to help traders size positions correctly.


## Sample Output: Stress Analysis

The tool generates a "Stress Analysis" chart, measuring the Mean Absolute Daily % Price Change for the 5 days leading up to and following the report.

**Key Insight**: As seen in the generated analysis above, volatility significantly expands immediately following the release (Day +1 to +5), with daily moves averaging >1.7%, compared to ~1.0-1.4% in the days prior.


## Datasets & Tech Stack

### Data Sources

- **Primary Data**: USDA WASDE Reports (Excel/CSV).
- **Market Data**: Yahoo Finance API (yfinance) for CBOT Wheat Futures (ZW=F).

### Technical Implementation

- **pandas & openpyxl**: Used for ETL (Extract, Transform, Load). The parser locates specific rows ("Ending Stocks") within multi-sheet Excel files using string matching, making it robust against minor format changes.

- **yfinance**: Fetches OHLC price data dynamically based on the report dates extracted.

- **matplotlib**: Renders the event study visualization, color-coding pre-event (red) and post-event (green) volatility.


## Installation & Usage

### 1. Environment Setup

Clone the repository and install the dependencies.

```bash
# Clone the repo
git clone https://github.com/yourusername/wasde-wheat-tool.git
cd wasde-wheat-tool

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install requirements
pip install pandas yfinance matplotlib openpyxl
```

### 2. Add Data

This tool is designed to work on the day of release.

1. Download the latest WASDE Report (Excel or CSV) from the [USDA Website](https://www.usda.gov/oce/commodity/wasde).
2. Drop the file directly into the `data/raw/` folder.

**Note**: The script automatically detects the newest file in this directory.

### 3. Run Analysis

Execute the main script to parse the data and generate the chart.

```bash
python main.py
```

## 📈 Logic Overview (How it works)

1. **Ingestion**: `main.py` scans `data/raw/` for the latest file.

2. **Extraction**: `wasde_parser.py` reads the file. It searches for the text "Ending Stocks" in the US and World Wheat tables to find the exact cell values.

3. **Data Fetching**: The script determines the publication date and fetches ±20 days of Wheat Futures data using yfinance.

4. **Computation**: It calculates the absolute percentage return for Day -5 through Day +5 relative to the publication date.

5. **Visualization**: It plots the mean absolute returns to visualize the "Event Premium" traders should expect.