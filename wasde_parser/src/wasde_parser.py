"""WASDE Parser - Extract Ending Stocks"""
import os
import re
import pandas as pd
from datetime import date

def find_latest_wasde_file(raw_dir):
    files = [f for f in os.listdir(raw_dir) if f.lower().endswith(('.csv', '.xlsx', '.xls'))]
    return os.path.join(raw_dir, files[0]) if files else None

def extract_ending_stocks(wasde_file, publication_date=None):
    if wasde_file.endswith('.csv'):
        df_us = df_world = pd.read_csv(wasde_file, header=None)
    else:
        excel = pd.ExcelFile(wasde_file)
        for s in excel.sheet_names:
            df_check = pd.read_excel(wasde_file, sheet_name=s, header=None, nrows=10).astype(str).values.flatten()
            if 'u.s. wheat' in ' '.join(df_check).lower():
                df_us = pd.read_excel(wasde_file, sheet_name=s, header=None)
            if 'world wheat' in ' '.join(df_check).lower():
                df_world = pd.read_excel(wasde_file, sheet_name=s, header=None)
    
    df_str = df_us.astype(str).apply(lambda r: ' '.join(r.values).lower(), axis=1)
    ending_idx = df_str[df_str.str.contains('ending stocks', na=False)].index[0]
    us_stocks = float(pd.to_numeric(df_us.iloc[ending_idx], errors='coerce').dropna()[lambda x: x >= 0].iloc[-1])
    
    df_str = df_world.astype(str).apply(lambda r: ' '.join(r.values).lower(), axis=1)
    world_idx = df_world.iloc[:, 0].astype(str).str.lower().str.contains('world.*3/', na=False, regex=True).idxmax()
    world_stocks = float(pd.to_numeric(df_world.iloc[world_idx + 1], errors='coerce').dropna().iloc[-1])
    
    if publication_date is None:
        match = re.search(r'wasde(\d{2})(\d{2})', os.path.basename(wasde_file).lower())
        month, year = (int(match.group(1)), 2000 + int(match.group(2))) if match else (1, 2024)
        publication_date = f"{year}-{month:02d}-01"
    
    return {
        'publication_date': pd.to_datetime(publication_date).date(),
        'us_ending_stocks': us_stocks,
        'world_ending_stocks': world_stocks,
        'file_name': os.path.basename(wasde_file)
    }
