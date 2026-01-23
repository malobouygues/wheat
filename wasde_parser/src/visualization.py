"""Visualization - Plot stress analysis"""
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
from .price_loader import load_wheat_prices

def plot_wasde_stress_analysis(history_file):
    hist = pd.read_csv(history_file)
    hist['publication_date'] = pd.to_datetime(hist['publication_date'])
    if hist.empty:
        return
    
    event_days = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    min_date = hist['publication_date'].min() - timedelta(days=20)
    max_date = hist['publication_date'].max() + timedelta(days=20)
    prices = load_wheat_prices(min_date, max_date)
    
    abs_returns = {day: [] for day in event_days}
    for _, row in hist.iterrows():
        pub = row['publication_date'].date()
        mask = prices['date'] >= pub
        if not mask.any():
            continue
        pub_idx = prices[mask].index[0]
        prices_dict = {d: prices.iloc[pub_idx + d]['close'] if 0 <= pub_idx + d < len(prices) else None for d in event_days + [-6, 0, 6]}
        
        for day in event_days:
            prev_day = -6 if day == -5 else (0 if day == 1 else day - 1)
            if prices_dict.get(prev_day) and prices_dict.get(day) and prices_dict[prev_day] > 0:
                abs_returns[day].append(abs((prices_dict[day] - prices_dict[prev_day]) / prices_dict[prev_day]) * 100)
    
    mean_abs = {day: sum(abs_returns[day]) / len(abs_returns[day]) if abs_returns[day] else 0 for day in event_days}
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['#e74c3c' if d < 0 else '#2ecc71' for d in event_days]
    bars = ax.bar(event_days, [mean_abs[d] for d in event_days], color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='WASDE Release (Day 0)')
    ax.set_xlabel('Event Day (Trading Days Relative to WASDE Release)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Mean Absolute Daily % Price Change', fontsize=12, fontweight='bold')
    ax.set_title('WASDE Stress Analysis: Mean Absolute Daily Returns Around Publication Dates', fontsize=14, fontweight='bold')
    ax.set_xticks(event_days)
    ax.set_xticklabels([f'{d:+d}' for d in event_days])
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()
    for bar, val in zip(bars, [mean_abs[d] for d in event_days]):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{val:.2f}%', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()
