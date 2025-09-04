# real-time-sales-forecasting/src/predict.py
import os
import pandas as pd
import joblib
import statsmodels.api as sm

def forecast_sales(df):
    """
    Generate a 7-day sales forecast using the trained ARIMA model.
    Args:
        df (pd.DataFrame): DataFrame with 'date' index and 'sales' column.
    Returns:
        pd.DataFrame: DataFrame with forecasted dates and sales.
    """
    model_path = '/var/task/sales_forecast.pkl' if os.path.exists('/var/task/sales_forecast.pkl') else os.path.join(os.path.dirname(__file__), '..', 'model', 'sales_forecast.pkl')
    try:
        model = joblib.load(model_path)
    except Exception as e:
        raise Exception(f"Failed to load model: {e}")

    # Forecast next 7 days
    forecast = model.forecast(steps=7)
    forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=7, freq='D')
    forecast_df = pd.DataFrame({'date': forecast_dates, 'sales': forecast})
    forecast_df['date'] = forecast_df['date'].dt.strftime('%Y-%m-%d')
    return forecast_df

if __name__ == "__main__":
    # Mock data for testing
    from utils import load_and_preprocess_data
    df = load_and_preprocess_data('data/processed/cleaned_sales_data.csv')
    forecast_df = forecast_sales(df)
    print(forecast_df)