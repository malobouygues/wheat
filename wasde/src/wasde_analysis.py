import pandas as pd


def compute_stocks_to_use(df):
    df = df.copy()
    df['us_stocks_to_use'] = df['us_ending_stocks'] / df['us_total_use']
    df['world_stocks_to_use'] = df['world_ending_stocks'] / df['world_total_use']
    return df


def compute_monthly_averages(df):
    df = df.copy()
    df['month'] = df['date'].dt.month
    
    us_avg = df.groupby('month')['us_stocks_to_use'].mean().reset_index()
    us_avg.columns = ['month', 'stocks_to_use']
    
    world_avg = df.groupby('month')['world_stocks_to_use'].mean().reset_index()
    world_avg.columns = ['month', 'stocks_to_use']
    
    return us_avg, world_avg
