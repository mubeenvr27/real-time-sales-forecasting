import pandas as pd
import statsmodels.api as sm
import joblib
import plotly.graph_objects as go
import plotly.io as pio
import os
from sklearn.metrics import mean_absolute_error
import itertools
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set Plotly renderer to PNG for Docker compatibility
pio.renderers.default = 'png'

def load_and_preprocess_data():
    df = pd.read_csv('data/processed/cleaned_sales_data.csv')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Handle invalid dates
    if df['date'].isna().any():
        raise ValueError("Some dates could not be parsed. Check 'date' column in cleaned_sales_data.csv")
    df.set_index('date', inplace=True)
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("Index is not a DatetimeIndex")
    df = df.asfreq('D', method='ffill')  # Set frequency to daily, forward-fill missing dates
    return df

def train_arima_model(df, forecast_horizon=7):
    # Split data: train (all but last 30 days), test (last 30 days)
    train = df['sales'][:-30]
    test = df['sales'][-30:]

    # Define parameter ranges for grid search
    p = range(0, 6)  # AR terms: 0 to 5
    d = range(0, 3)  # Differencing: 0 to 2
    q = range(0, 3)  # MA terms: 0 to 2
    pdq = list(itertools.product(p, d, q))  # All combinations

    best_mae = float('inf')
    best_order = None
    best_model = None

    # Grid search for best ARIMA parameters
    for order in pdq:
        try:
            model = sm.tsa.ARIMA(train, order=order)
            fitted_model = model.fit()
            forecast = fitted_model.forecast(steps=forecast_horizon)
            mae = mean_absolute_error(test[:forecast_horizon], forecast)
            if mae < best_mae:
                best_mae = mae
                best_order = order
                best_model = fitted_model
            print(f"Order {order}: MAE = {mae:.2f}")
        except:
            continue

    print(f"Best ARIMA order: {best_order} with MAE: {best_mae:.2f}")

    # Save the best model
    os.makedirs('model', exist_ok=True)
    joblib.dump(best_model, 'model/sales_forecast.pkl')

    # Plot actual vs fitted values for training data
    fitted_values = best_model.fittedvalues
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=train.index, y=train, name='Actual Sales'))
    fig1.add_trace(go.Scatter(x=train.index, y=fitted_values, name='Fitted Sales'))
    fig1.update_layout(title=f'ARIMA{best_order}: Actual vs Fitted Sales (2023-2024)', xaxis_title='Date', yaxis_title='Sales')
    os.makedirs('data/processed/plots', exist_ok=True)
    fig1.write_image('data/processed/plots/arima_fitted.png')
    print("Saved plot: data/processed/plots/arima_fitted.png")

    # Forecast 7 days (for next-week prediction) and compare with test set
    forecast = best_model.forecast(steps=forecast_horizon)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=test[:forecast_horizon], name='Actual Sales'))
    fig2.add_trace(go.Scatter(x=test.index[:forecast_horizon], y=forecast, name='Forecasted Sales'))
    fig2.update_layout(title=f'ARIMA{best_order}: {forecast_horizon}-Day Test Set Forecast (2023-2024)', xaxis_title='Date', yaxis_title='Sales')
    fig2.write_image('data/processed/plots/arima_forecast.png')
    print("Saved plot: data/processed/plots/arima_forecast.png")

    # Calculate and print MAE for the best model
    mae = mean_absolute_error(test[:forecast_horizon], forecast)
    print(f"Final MAE for best model (order {best_order}): {mae:.2f}")

    return best_model

if __name__ == "__main__":
    df = load_and_preprocess_data()
    model = train_arima_model(df, forecast_horizon=7)
    print("Model trained and saved to model/sales_forecast.pkl")
    print(model.summary())