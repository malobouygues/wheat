import os
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

output_dir = "/Users/malo/PythonProjects/github/wheat/calendar-spreads/data"
start_year = 2015
end_year = 2015

os.makedirs(output_dir, exist_ok=True)

tv = TvDatafeed()

for year in range(start_year, end_year + 1):
    ticker = f"ZWN{year}"
    filename = f"ZWN{year}.csv"
    filepath = os.path.join(output_dir, filename)
    
    df = tv.get_hist(
        symbol=ticker,
        exchange="CBOT",
        interval=Interval.in_daily,
        n_bars=5000
    )
    
    if df is not None and not df.empty:
        df = df.reset_index()
        df['datetime'] = pd.to_datetime(df['datetime']).dt.date
        df = df[['datetime', 'close', 'volume']]
        df.to_csv(filepath, index=False, header=False)
        print(f"{ticker}: {len(df)} rows saved")
