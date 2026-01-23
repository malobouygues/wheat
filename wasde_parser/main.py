"""WASDE Wheat - Junior Trader Style"""
import os
import re
import pandas as pd
from src.wasde_parser import find_latest_wasde_file, extract_ending_stocks
from src.price_loader import display_prices_around_publications
from src.visualization import plot_wasde_stress_analysis

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('data/raw', exist_ok=True)

wasde_file = find_latest_wasde_file('data/raw')
if not wasde_file:
    print("ERROR: No WASDE file found in data/raw/")
    exit()

file_name = os.path.basename(wasde_file)
match = re.search(r'wasde(\d{2})(\d{2})', file_name.lower())
if match:
    month, year = int(match.group(1)), 2000 + int(match.group(2))
else:
    month, year = 1, 2024

history_file = 'data/wasde_wheat_history.csv'
hist = pd.read_csv(history_file) if os.path.exists(history_file) else pd.DataFrame(columns=['publication_date', 'us_ending_stocks', 'world_ending_stocks', 'file_name'])
hist['publication_date'] = pd.to_datetime(hist['publication_date'])

if not hist.empty and ((hist['publication_date'].dt.year == year) & (hist['publication_date'].dt.month == month)).any():
    print(f"WASDE {year}-{month:02d} already processed, skipping extraction")
else:
    pub_date = input(f"Date de publication pour {file_name} (YYYY-MM-DD): ").strip() or None
    data = extract_ending_stocks(wasde_file, pub_date)
    print(f"Found: {data['file_name']} | Date: {data['publication_date']}")
    print(f"US: {data['us_ending_stocks']:.0f}M bu | World: {data['world_ending_stocks']:.0f}M tonnes")
    
    hist = pd.concat([hist, pd.DataFrame([data])], ignore_index=True)
    hist = hist.sort_values('publication_date').reset_index(drop=True)
    hist.to_csv(history_file, index=False)
    print(f"Saved to {history_file}")

hist = pd.read_csv(history_file)
hist['publication_date'] = pd.to_datetime(hist['publication_date'])
hist = hist.sort_values('publication_date').reset_index(drop=True)
if len(hist) >= 2:
    print(f"US MoM: {hist['us_ending_stocks'].diff().iloc[-1]:+.0f}M bu | World MoM: {hist['world_ending_stocks'].diff().iloc[-1]:+.0f}M tonnes")

display_prices_around_publications(history_file)

print("\nGenerating WASDE stress analysis chart...")
plot_wasde_stress_analysis(history_file)
