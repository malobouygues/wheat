# Wheat Seasonality & Spread Analysis (CBOT)

## 🎯 Project Objective

This project was designed to analyze the seasonal cycles of Soft Red Winter Wheat (SRW) on the Chicago Board of Trade (CBOT). While the initial goal was to visualize "Flat Price" seasonality, the analysis evolved to focus on Calendar Spreads, which constitute the core decision-making metric for physical merchants managing storage assets.

## 🧠 The Pivot: From Speculation to Merchant Logic

### 1. Initial Approach: Directional (Flat Price)

- Initially, the script was built to identify bullish/bearish windows on the nominal price.
- **Observation**: While trends exist, the "Flat" price is too heavily influenced by exogenous shocks (geopolitics, inflation) to be traded solely based on seasonality.
- **Limitation**: Physical players (like Louis Dreyfus) are typically hedged and do not speculate on the raw direction of the market.

### 2. Professional Approach: Structural (Term Structure)

- The project now focuses on Market Structure (Contango/Backwardation) via inter-month spreads.
- **Rationale**: For a storage operator, the critical variable is not the price, but the Carry (the price difference that remunerates storage).
- **Focus**: Analysis of the July (N) vs. December (Z) spread.

## 🧠 Key Learnings & Iterations: "Trading the Rule, Not the Exception"

During the development of this tool, I moved from a naive data analysis approach to a logic adapted to market realities. I identified two critical flaws in standard seasonality calculations:

### 1. The "Price Level" Bias (Inflation)
- **Initial Mistake**: My first iteration averaged raw prices.
- **Realization**: A $0.50 move in 2000 (when Wheat was ~$2.50) is statistically crushed by daily volatility in 2022 (when Wheat was ~$8.00). Recent high-priced years were disproportionately influencing the average.
- **Correction**: I switched to **Base-100 Indexing** to compare *percentage returns* rather than nominal dollar moves.

### 2. The "Outlier" Bias (Mean vs. Median)
- **Initial Mistake**: Using an arithmetic mean included extreme events that are not seasonal.
- **Realization**: I want to identify the recurring behavior of the market (the rule), not the impact of one-off crises (the exception).
- **Correction**: I implemented the **Median** to naturally filter out "Black Swan" events without having to manually curve-fit the data.

## 🛠 Methodology & Technical Choices

To make 10 years of data comparable despite drastically different price levels, several transformations were applied:

### 1. Marketing Year Alignment

- Wheat does not follow the calendar year.
- **Implementation**: The code forces the start of the year to June 1st (US harvest start) and the end to May 31st.
- **Why?** To align the analysis with the actual biological and logistical cycle of the commodity.

#### The "Marketing Year" Logic: Why June 1st?

**The Economic Necessity**: Using a standard Calendar Year (Jan–Dec) for agricultural commodities is not just arbitrary; it creates a false signal.

**The Supply Reset**: June 1st marks the beginning of the Soft Red Winter (SRW) wheat harvest. This is the fundamental moment when the balance sheet resets, and new physical supply floods the market.

**The "Jan 1st" Problem**: In January, wheat has already been sitting in silos for six months. If we reset the price index to 100 on January 1st (as a standard YoY analysis would), we mathematically erase the Cost of Carry (storage costs + interest) that has been priced into the market since the summer. By starting on June 1st, the model captures the full lifecycle of the crop from the combine harvester to the end of the storage season.

### 2. Time Horizon: Active vs. Dormant Liquidity

The model filters price data based on Time to Maturity.

The "Dormant" Phase (Year N-1): We exclude data for the spread (e.g., ZWN2015 - ZWZ2015) recorded in 2014. During this period, the spread is speculative, illiquid, and disconnected from physical storage pressures.

The "Active" Phase (Year N): The analysis isolates the April to June window of the expiration year. This captures the "Delivery Pressure" phase where the spread tightens based on actual harvest realization.

### 3. Execution Constraints: First Notice Day & Delivery Risk

The analysis cutoff date is strictly dictated by the CME Group Contract Specifications regarding physical delivery. The model enforces a hard stop to avoid the "Delivery Phase," where price action decouples from broad market supply/demand to focus on specific logistical convergence.

First Notice Day (FND) Definition: According to the official CME Group Calendar, the First Notice Day—the date on which the Exchange may issue delivery assignment notices to long position holders—is defined as the last business day of the month preceding the contract month.

Example: For the July 2026 contract (WN26), the CME schedule confirms the First Notice Day is June 30, 2026.

Operational Logic: To ensure the analysis reflects a liquid, speculative spread rather than a physical settlement process, the algorithm terminates the data series prior to the FND. This eliminates the risk of Physical Assignment and filters out the volatility associated with the expiration of the front-month contract.

https://www.cmegroup.com/markets/agriculture/grains/wheat.calendar.html

### 4. Algorithmic Safety: The [-3] Index Rule

To automate this safety buffer across different years without hardcoding dates (which fail due to weekends/holidays), the script uses relative indexing:

Logic: Month_Trading_Days[-3]

Effect: The code dynamically identifies all trading days in June for a given year and selects the 3rd to last session. This ensures the analysis consistently terminates ~2 days before the First Notice Day, protecting the integrity of the dataset from delivery-related volatility.

### 5. Normalization (Base 100 Indexing)

- **Problem**: Comparing a year trading at 400 cents (2016) with a year trading at 1200 cents (2022) skews simple averages.
- **Solution**: Each year is rebased to 100 on the first day of the campaign (indexed_price). This allows for comparing relative performance rather than absolute values.

### 6. Statistical Smoothing (Gaussian Filter)

- **Technique**: Usage of `scipy.ndimage.gaussian_filter1d` (Sigma = 3).
- **Objective**: To eliminate high-frequency noise (daily volatility) to reveal the underlying trend (the seasonal signal) without introducing excessive lag, unlike a simple moving average.

### 7. Central Metric: The Median (Handling Black Swans)

- **Choice**: Preference for the Median over the Mean.

- **Reason**: Grain markets are prone to extreme shocks (e.g., Ukraine War 2022). The 
mean is too sensitive to these outliers, whereas the median better represents the 
behavior of a "standard year."

The choice of the Median over the Mean was driven by the analysis of three specific structural outliers identified in the dataset. Including these in a simple average would create false seasonal signals:

* **2022 (Violet Curve) - The Geopolitical Shock**:
    * *Context*: The invasion of Ukraine by Russia.
    * *Movement*: A massive exogenous supply shock starting ~Day 50 (late Feb) and peaking ~Day 70 (March).
    * *Why exclude it?* This is a war event, not a weather or harvest cycle. Including it would falsely train the model to expect a price explosion in February.

* **2007/2008 (Pale Green Curve) - The "Agflation" Bubble**:
    * *Context*: The global food crisis and frantic speculation preceding the subprime crash.
    * *Movement*: A parabolic rise where prices doubled (Index 100 to 200).
    * *Why exclude it?* This depicts a speculative bubble followed by a crash, a non-reproducible financial phenomenon.

* **2010 (Bright Green Curve) - The Climatic Shock**:
    * *Context*: The "Great Russian Drought" and the subsequent export ban.
    * *Movement*: A sharp spike around Day 180-200 (July/August).
    * *Analysis*: While weather is part of seasonality, the magnitude here (driven by a political embargo) was extreme.

**Conclusion**: The Median provides a robust signal that ignores these extreme tails to focus on the "standard year" behavior.

#### Seasonal Theory: The Narrative of a "Normal" Year

While the Median filters out outliers (wars, bubbles), it also reveals the narrative of a standard marketing year. The code visualizes three distinct fundamental phases:

**Harvest Pressure (June – July)**:

*The Low Point*: Farmers often sell off the combine to clear space or generate cash flow. This "heavy cash selling" creates a temporary glut, historically suppressing prices to their seasonal lows.

**The Cost of Carry (August – December)**:

*The Mechanical Grind*: Once the harvest pressure subsides, the price must theoretically rise to cover the costs of storing the grain (storage fees + interest rates). This is the Contango phase, where the market pays participants to hold the inventory.

**The Weather Premium (February – May)**:

*The Volatility Zone*: As Winter Wheat breaks dormancy, the crop becomes vulnerable to late freezes or drought. The market prices in a "Risk Premium" until the yield potential is confirmed, often leading to a seasonal rally or increased volatility before the next harvest.

## 📊 Spread Analysis: Case Study July (N) vs. Dec (Z)

The tool specifically analyzes the spread between New Crop (July - N) and Old Crop (December - Z).

**Why this choice?**

- **July (N)**: Corresponds to the massive arrival of the winter harvest (Harvest Pressure). It is often the relative low point of the forward curve.
- **December (Z)**: Corresponds to a period of pure consumption (Storage).

**Investment Thesis**: During the harvest, the market must incentivize storage. We analyze if the Carry (Spread Z - N) historically widens between May and July, offering a "Cash & Carry" opportunity.

#### Deep Dive: The July (N) vs. Dec (Z) Spread

This specific spread is the industry standard for measuring the "Health of the Carry."

**July (N) – The New Crop Anchor**: This contract represents the arrival of the new harvest. It reflects the immediate abundance of fresh supply.

**December (Z) – The Storage Anchor**: This contract represents grain that has been stored for ~6 months.

**The Arbitrage Signal (The "Trade")**:

*Full Carry Scenario (Wide Z-N Spread)*: When December trades significantly higher than July, the market is incentivizing storage. It signals an oversupply where the market pays merchants to buy physical wheat in July, store it, and hedge it against December (a "Cash & Carry" trade).

*Backwardation Scenario (Narrow or Negative Z-N Spread)*: When July trades higher than December, it signals an immediate shortage. The market is penalizing storage and demanding immediate delivery, effectively telling merchants: "Don't store it, we need it now."

## 💾 Data Engineering & Pipeline

The data acquisition pipeline prioritizes stability and reproducibility over web scraping.

- **Source**: TradingView API (via `tvDatafeed` Python wrapper). This bypasses the need for fragile HTML scraping of the CME website.

### Automated Extraction:

- The script dynamically generates ticker symbols for specific expirations (e.g., ZWZ2020, ZWN2020) using a loop over the target years (2016–2027).
- It utilizes `tv.get_hist` to fetch deep historical data (up to 5000 bars) directly from CBOT.

### Data Structure:

- Data is cleaned and standardized immediately upon extraction.
- The datetime index is reset to a column to ensure proper serialization.
- **Storage**: Individual CSV files per contract (e.g., ZWZ2021.csv) containing datetime, close, and volume.

### Date Handling:

- The pipeline preserves the datetime objects returned by the API during the transition to CSV, ensuring that subsequent analysis scripts can easily parse dates without ambiguity (ISO format compliant).

## 🚀 Roadmap

- **Basis Analysis**: Integrate Cash data to calculate the real Basis (Cash - Futures).
- **Volatility Cones**: Add volatility analysis to evaluate if options are expensive or cheap relative to the season.
- **COT Report**: Overlay "Managed Money" positioning to see if price seasonality correlates with speculative flows.
