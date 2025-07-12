import pandas as pd
import numpy as np

def generate_sales_data():
    dates = pd.date_range(start='2023-01-01', end='2025-07-29', freq='D')
    base_sales = np.random.poisson(lam=30, size=len(dates))
    # Add weekly seasonality (higher sales on weekends)
    seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
    sales = base_sales + seasonality + np.random.normal(0, 5, len(dates))
    sales = np.clip(sales, 10, 100).astype(int)  # Ensure realistic sales
    df = pd.DataFrame({'date': dates, 'sales': sales, 'stock': sales * 2})  # Stock starts at 2x daily sales
  #  df.to_csv('data/raw/sales_data.csv', index=False)
    return df

if __name__ == "__main__":
    df = generate_sales_data()
    df.head()