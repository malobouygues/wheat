import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

from src.calendar_spreads import calculate_spread_for_year, calculate_historical_median

script_dir = os.path.dirname(os.path.abspath(__file__))
historical_years = list(range(2015, 2026))
current_year = 2026

historical_spreads = []
for year in historical_years:
    df_spread = calculate_spread_for_year(year)
    if df_spread is not None and len(df_spread) > 0:
        historical_spreads.append(df_spread)

df_current = calculate_spread_for_year(current_year)

if len(historical_spreads) == 0:
    print("No historical data available")
else:
    df_median = calculate_historical_median(historical_spreads)
    
    plt.figure(figsize=(12, 6))
    
    plt.plot(df_median['plot_date'], df_median['median_spread'], 
             label='Historical Median (2015-2025)', color='black', linewidth=2)
    
    if df_current is not None and len(df_current) > 0:
        plt.plot(df_current['plot_date'], df_current['normalized_spread'], 
                 label='Current Year (2026)', color='red', linewidth=2)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('Wheat Calendar Spread: July - December (ZWN - ZWZ)', fontsize=12, fontweight='bold')
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Normalized Spread (cents)', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
