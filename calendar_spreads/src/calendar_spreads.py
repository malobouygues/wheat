import pandas as pd
import numpy as np

def load_contract_data(year, contract_code):
    file_path = f"/Users/malo/PythonProjects/github/wheat/calendar_spreads/data/{contract_code}{year}.csv"
    df = pd.read_csv(file_path, header=None, names=['date', 'price', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df[['date', 'price']]

def get_june_end_date(df, year):
    june_data = df[(df['date'].dt.year == year) & (df['date'].dt.month == 6)]
    if len(june_data) < 3:
        return june_data['date'].max() if len(june_data) > 0 else None
    june_dates = sorted(june_data['date'].unique())
    return june_dates[-3]

def calculate_spread_for_year(year):
    zwn = load_contract_data(year, 'ZWN')
    zwz = load_contract_data(year, 'ZWZ')
    
    merged = pd.merge(zwn, zwz, on='date', suffixes=('_zwn', '_zwz'))
    merged['spread'] = merged['price_zwn'] - merged['price_zwz']
    
    april_start = pd.Timestamp(f"{year}-04-01")
    end_date = get_june_end_date(merged, year)
    
    if end_date is None:
        return None
    
    filtered = merged[(merged['date'] >= april_start) & (merged['date'] <= end_date)].copy()
    
    if len(filtered) == 0:
        return None
    
    june_first = pd.Timestamp(f"{year}-06-01")
    
    data_before = filtered[filtered['date'] < june_first]
    data_after = filtered[filtered['date'] >= june_first]
    
    if len(data_before) == 0 or len(data_after) == 0:
        return None
        
    point_prev = data_before.iloc[-1]
    point_next = data_after.iloc[0]
    
    total_gap_days = (point_next['date'] - point_prev['date']).days
    days_to_target = (june_first - point_prev['date']).days
    
    spread_diff = point_next['spread'] - point_prev['spread']
    theoretical_june_val = point_prev['spread'] + (spread_diff * (days_to_target / total_gap_days))
    
    filtered['normalized_spread'] = filtered['spread'] - theoretical_june_val
    
    filtered['plot_date'] = filtered['date'].apply(lambda x: x.replace(year=2000))
    
    return filtered[['plot_date', 'normalized_spread']]

def calculate_historical_median(historical_spreads):
    all_data = pd.concat(historical_spreads, ignore_index=True)
    
    grouped = all_data.groupby('plot_date')['normalized_spread'].median().reset_index()
    grouped = grouped.sort_values('plot_date')
    
    window = 5
    values = grouped['normalized_spread'].values
    smoothed = np.convolve(values, np.ones(window)/window, mode='same')
    grouped['median_spread'] = smoothed
    
    return grouped[['plot_date', 'median_spread']]