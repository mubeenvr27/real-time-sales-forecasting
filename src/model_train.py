import pandas as pd
import statsmodels.api as sm
import joblib
import plotly.graph_objects as go
import plotly.io as pio
import os
from sklearn.metrics import mean_absolute_error

# Set Plotly renderer to PNG for Docker compatibility
pio.renderers.default = 'png'

def load_and_preprocess_data():
    df = pd.read_csv('data/processed/cleaned_sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def train_arima_model(df, order=(5, 1, 0)):
    # Split data: train (all but last 30 days), test (last 30 days)
    train = df['sales'][:-30]
    test = df['sales'][-30:]

    # Train ARIMA model on train set
    model = sm.tsa.ARIMA(train, order=order)
    fitted_model = model.fit()

    # Save the model
    os.makedirs('model', exist_ok=True)
    joblib.dump(fitted_model, 'model/sales_forecast.pkl')

    # Plot actual vs fitted values for training data
    fitted_values = fitted_model.fittedvalues
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=train.index, y=train, name='Actual Sales'))
    fig1.add_trace(go.Scatter(x=train.index, y=fitted_values, name='Fitted Sales'))
    fig1.update_layout(title='ARIMA Model: Actual vs Fitted Sales (2023-2024)', xaxis_title='Date', yaxis_title='Sales')
    os.makedirs('data/processed/plots', exist_ok=True)
    fig1.write_image('data/processed/plots/arima_fitted.png')
    print("Saved plot: data/processed/plots/arima_fitted.png")

    # Forecast 30 days and compare with test set
    forecast = fitted_model.forecast(steps=30)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=test.index, y=test, name='Actual Sales'))
    fig2.add_trace(go.Scatter(x=test.index, y=forecast, name='Forecasted Sales'))
    fig2.update_layout(title='ARIMA: 30-Day Test Set Forecast (2023-2024)', xaxis_title='Date', yaxis_title='Sales')
    fig2.write_image('data/processed/plots/arima_forecast.png')
    print("Saved plot: data/processed/plots/arima_forecast.png")

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(test, forecast)
    print(f"MAE: {mae:.2f}")

    return fitted_model

if __name__ == "__main__":
    df = load_and_preprocess_data()
    model = train_arima_model(df)
    print("Model trained and saved to model/sales_forecast.pkl")
    print(model.summary())