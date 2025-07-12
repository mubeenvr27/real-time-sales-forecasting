import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

# Set Plotly renderer to PNG for Docker compatibility
pio.renderers.default = 'png'

def generate_sales_data():
    # Generate two years of daily data (2023-01-01 to 2024-12-31)
    dates = pd.date_range(start='2023-01-01', end='2025-07-31', freq='D')
    base_sales = np.random.poisson(lam=30, size=len(dates))
    # Add weekly seasonality (higher sales on weekends)
    seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    sales = base_sales + seasonality + np.random.normal(0, 5, len(dates))
    sales = np.clip(sales, 10, 100).astype(int)  # Ensure realistic sales
    df = pd.DataFrame({'date': dates, 'sales': sales, 'stock': sales * 2})
    # Ensure output directory exists
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/sales_data.csv', index=False)
    print(f"Synthetic sales data saved to data/raw/sales_data.csv")
    return df

def perform_eda(df):
    # Ensure output directory for plots exists
    os.makedirs('data/processed/plots', exist_ok=True)
    
    # Check for nulls
    print("Missing values:\n", df.isnull().sum())
    
    # Basic stats
    print("\nSummary statistics:\n", df.describe())
    
    # Plot 1: Daily Sales Trend
    fig1 = px.line(df, x='date', y='sales', title='Daily Sales Trend (2023-2025)')
    fig1.update_layout(xaxis_title='Date', yaxis_title='Sales')
    fig1.write_image('data/processed/plots/daily_sales.png')
    print("Saved plot: data/processed/plots/daily_sales.png")
    
    # Plot 2: Weekly Moving Average
    df['sales_ma7'] = df['sales'].rolling(window=7).mean()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['date'], y=df['sales'], name='Daily Sales'))
    fig2.add_trace(go.Scatter(x=df['date'], y=df['sales_ma7'], name='7-Day Moving Average'))
    fig2.update_layout(title='Sales with 7-Day Moving Average (2023-2025)', xaxis_title='Date', yaxis_title='Sales')
    fig2.write_image('data/processed/plots/sales_ma7.png')
    print("Saved plot: data/processed/plots/sales_ma7.png")

def clean_data(df):
    # Remove any nulls (unlikely in synthetic data)
    df = df.dropna()
    # Ensure output directory exists
    os.makedirs('data/processed', exist_ok=True)
    # Save cleaned data
    df.to_csv('data/processed/cleaned_sales_data.csv', index=False)
    print("Cleaned data saved to data/processed/cleaned_sales_data.csv")
    return df

if __name__ == "__main__":
    df = generate_sales_data()
    print("Generated Data (first 5 rows):\n", df.head())
    perform_eda(df)
    df_cleaned = clean_data(df)