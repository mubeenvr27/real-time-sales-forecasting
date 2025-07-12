import pandas as pd
import joblib
from utils import load_and_preprocess_data
import os

def forecast_sales(model_path='model/sales_forecast.pkl', steps=7, input_data_path='data/processed/cleaned_sales_data.csv'):
    """
    Generate a 7-day sales forecast using the trained ARIMA model.

    Args:
        model_path (str): Path to the trained model file (default: 'model/sales_forecast.pkl').
        steps (int): Number of days to forecast (default: 7 for weekly forecast).
        input_data_path (str): Path to the input sales data (default: 'data/processed/cleaned_sales_data.csv').

    Returns:
        pd.DataFrame: DataFrame with forecast dates and predicted sales.
    """
    # Check if model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    # Load the trained model
    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise ValueError(f"Error loading model from {model_path}: {str(e)}")

    # Load and preprocess data to get the last date
    try:
        df = load_and_preprocess_data()  # Uses your utils function
    except Exception as e:
        raise ValueError(f"Error loading data from {input_data_path}: {str(e)}")

    # Ensure the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a DatetimeIndex")

    # Get the last date from the dataset
    last_date = df.index.max()
    if pd.isna(last_date):
        raise ValueError("No valid dates found in the dataset")

    # Generate forecast
    try:
        forecast = model.forecast(steps=steps)
    except Exception as e:
        raise ValueError(f"Error generating forecast: {str(e)}")

    # Create date range for forecast (starting the day after the last date)
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=steps, freq='D')

    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecasted_sales': forecast
    })
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])

    # Save forecast to CSV
    output_path = 'data/processed/forecasted_sales.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    print(f"Forecast saved to {output_path}")

    return forecast_df

if __name__ == "__main__":
    try:
        forecast_df = forecast_sales()
        print("Forecasted Sales:\n", forecast_df)
    except Exception as e:
        print(f"Error during forecasting: {str(e)}")