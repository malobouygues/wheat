import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

from src.ratios import compute_stocks_to_use, compute_monthly_averages

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "data", "wasde_wheat_history.csv")

df = pd.read_csv(csv_path)
df['date'] = pd.to_datetime(df['date'])

df = compute_stocks_to_use(df)

last_date = df['date'].max()
cutoff_date = last_date - pd.DateOffset(years=5)
df_5y = df[df['date'] > cutoff_date]

df_us_long, df_world_long = compute_monthly_averages(df)
df_us_5y, df_world_5y = compute_monthly_averages(df_5y)

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

first_date = df['date'].min()
first_str = f"{month_names[first_date.month - 1]}-{first_date.strftime('%y')}"
last_str = f"{month_names[last_date.month - 1]}-{last_date.strftime('%y')}"
month_label = f'Month ({first_str} - {last_str})'

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(df_us_long['month'], df_us_long['stocks_to_use'], marker='o', linewidth=2, label='Long-Term Avg')
ax1.plot(df_us_5y['month'], df_us_5y['stocks_to_use'], linestyle='--', linewidth=2, color='gray', label='5Y Avg')
ax1.set_title('US Wheat Stocks-to-Use Ratio (Monthly Average)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Stocks-to-Use Ratio', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names)
ax1.legend()

ax2.plot(df_world_long['month'], df_world_long['stocks_to_use'], marker='o', linewidth=2, color='orange', label='Long-Term Avg')
ax2.plot(df_world_5y['month'], df_world_5y['stocks_to_use'], linestyle='--', linewidth=2, color='gray', label='5Y Avg')
ax2.set_title('World Wheat Stocks-to-Use Ratio (Monthly Average)', fontsize=12, fontweight='bold')
ax2.set_xlabel(month_label, fontsize=10)
ax2.set_ylabel('Stocks-to-Use Ratio', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(month_names)
ax2.legend()

plt.tight_layout()
plt.show()
