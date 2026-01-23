"""Price Loader - Fetch CBOT Wheat prices"""
import pandas as pd
import yfinance as yf
from datetime import timedelta

def load_wheat_prices(start_date, end_date):
    ticker = yf.Ticker('ZW=F')
    prices = ticker.history(period='max')
    dates_str = prices.index.strftime('%Y-%m-%d')
    dates = [pd.to_datetime(d).date() for d in dates_str]
    prices = pd.DataFrame({
        'date': dates,
        'close': prices['Close'].values
    })
    
    start = start_date.date() if hasattr(start_date, 'date') else start_date
    end = (end_date + timedelta(days=1)).date() if hasattr(end_date, 'date') else end_date + timedelta(days=1)
    mask = (prices['date'] >= start) & (prices['date'] <= end)
    return prices[mask].sort_values('date').reset_index(drop=True)

def display_prices_around_publications(history_file):
    hist = pd.read_csv(history_file)
    hist['publication_date'] = pd.to_datetime(hist['publication_date'])
    prices = load_wheat_prices(hist['publication_date'].min() - timedelta(days=15), hist['publication_date'].max() + timedelta(days=15))
    
    print("\n" + "="*100)
    print("ZW=F Prices Around WASDE Publication Dates")
    print("="*100)
    for _, row in hist.iterrows():
        pub = row['publication_date'].date()
        mask = prices['date'] >= pub
        if not mask.any():
            continue
        pub_idx = prices[mask].index[0]
        before = [prices.iloc[pub_idx + d]['close'] if 0 <= pub_idx + d < len(prices) else None for d in [-5, -4, -3, -2, -1]]
        after = [prices.iloc[pub_idx + d]['close'] if 0 <= pub_idx + d < len(prices) else None for d in [1, 2, 3, 4, 5]]
        print(f"\nPublication: {pub}")
        print(f"Before: {' | '.join([f'Day {d:+2d}: {p:.2f}' if p else f'Day {d:+2d}: N/A' for d, p in zip([-5, -4, -3, -2, -1], before)])}")
        print(f"After:  {' | '.join([f'Day {d:+2d}: {p:.2f}' if p else f'Day {d:+2d}: N/A' for d, p in zip([1, 2, 3, 4, 5], after)])}")
    print("="*100)
