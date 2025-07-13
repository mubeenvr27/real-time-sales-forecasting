import pandas as pd
import os

def load_and_preprocess_data(file_path='data/processed/cleaned_sales_data.csv'):
    """
    Load and preprocess sales data, ensuring daily frequency.

    Args:
        file_path (str): Path to the input CSV file (default: 'data/processed/cleaned_sales_data.csv').

    Returns:
        pd.DataFrame: Preprocessed DataFrame with DatetimeIndex and daily frequency.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")

    # Load data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {str(e)}")

    # Convert date to datetime
    if 'date' not in df.columns:
        raise ValueError("DataFrame must contain a 'date' column")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isna().any():
        raise ValueError("Some dates could not be parsed in 'date' column")

    # Set date as index
    df.set_index('date', inplace=True)

    # Ensure daily frequency with forward-fill for missing dates
    df = df.asfreq('D', method='ffill')

    # Check for required columns
    if 'sales' not in df.columns:
        raise ValueError("DataFrame must contain a 'sales' column")

    return df

def calculate_reorder_threshold(df, multiplier=1.5):
    """
    Calculate the reorder threshold based on average daily sales.

    Args:
        df (pd.DataFrame): DataFrame with 'sales' column.
        multiplier (float): Multiplier for average daily sales (default: 1.5).

    Returns:
        float: Reorder threshold (multiplier * average daily sales).
    """
    if 'sales' not in df.columns:
        raise ValueError("DataFrame must contain a 'sales' column")
    avg_daily_sales = df['sales'].mean()
    if pd.isna(avg_daily_sales):
        raise ValueError("Cannot calculate average daily sales: missing or invalid data")
    threshold = multiplier * avg_daily_sales
    return threshold

if __name__ == "__main__":
    try:
        df = load_and_preprocess_data()
        threshold = calculate_reorder_threshold(df)
        print(f"Reorder Threshold: {threshold:.2f} units")
    except Exception as e:
        print(f"Error: {str(e)}")