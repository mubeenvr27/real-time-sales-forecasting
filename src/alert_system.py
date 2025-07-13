import pandas as pd
import os
from utils import load_and_preprocess_data, calculate_reorder_threshold

def generate_inventory_alerts(historical_data_path='data/processed/cleaned_sales_data.csv',
                             forecast_data_path='data/processed/forecasted_sales.csv',
                             initial_stock=None, multiplier=1.5, first_alert_only=False):
    """
    Generate inventory alerts based on forecasted sales and reorder threshold.

    Args:
        historical_data_path (str): Path to historical sales data.
        forecast_data_path (str): Path to forecasted sales data.
        initial_stock (float): Initial stock level (default: None, uses last 'stock' from historical data).
        multiplier (float): Multiplier for reorder threshold (default: 1.5).
        first_alert_only (bool): If True, only generate the first alert (default: False).

    Returns:
        pd.DataFrame: DataFrame with alerts (date, stock, forecasted_sales, message).
    """
    # Check file existence
    if not os.path.exists(historical_data_path):
        raise FileNotFoundError(f"Historical data file not found at {historical_data_path}")
    if not os.path.exists(forecast_data_path):
        raise FileNotFoundError(f"Forecast data file not found at {forecast_data_path}")

    # Load historical and forecast data
    try:
        historical_df = load_and_preprocess_data(historical_data_path)
        forecast_df = pd.read_csv(forecast_data_path)
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

    # Validate forecast data
    if 'date' not in forecast_df.columns or 'forecasted_sales' not in forecast_df.columns:
        raise ValueError("Forecast DataFrame must contain 'date' and 'forecasted_sales' columns")
    forecast_df['date'] = pd.to_datetime(forecast_df['date'], errors='coerce')
    if forecast_df['date'].isna().any():
        raise ValueError("Some dates in forecast data could not be parsed")

    # Get initial stock level
    if initial_stock is None:
        if 'stock' not in historical_df.columns:
            raise ValueError("Historical DataFrame must contain a 'stock' column or initial_stock must be provided")
        initial_stock = historical_df['stock'].iloc[-1]
    
    # Calculate reorder threshold
    try:
        threshold = calculate_reorder_threshold(historical_df, multiplier=multiplier)
    except Exception as e:
        raise ValueError(f"Error calculating reorder threshold: {str(e)}")

    # Simulate stock depletion and generate alerts
    alerts = []
    current_stock = initial_stock
    for index, row in forecast_df.iterrows():
        date = row['date']
        forecasted_sales = row['forecasted_sales']
        if pd.isna(forecasted_sales):
            continue  # Skip invalid forecast values
        current_stock = max(0, current_stock - forecasted_sales)  # Cap stock at 0
        if current_stock < threshold:
            message = f"Low stock alert on {date.date()}: Stock ({current_stock:.2f}) below threshold ({threshold:.2f}). Reorder recommended."
            alerts.append({
                'date': date,
                'stock': current_stock,
                'forecasted_sales': forecasted_sales,
                'message': message
            })
            if first_alert_only:
                break  # Stop after first alert

    # Create alerts DataFrame
    alerts_df = pd.DataFrame(alerts)
    
    # Save alerts to CSV
    if not alerts_df.empty:
        output_path = 'data/processed/inventory_alerts.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        alerts_df.to_csv(output_path, index=False)
        print(f"Alerts saved to {output_path}")
    else:
        print("No inventory alerts triggered.")

    return alerts_df

if __name__ == "__main__":
    try:
        # Run with default stock
        print(f"Running with default stock and threshold (multiplier={1.5}):")
        alerts_df = generate_inventory_alerts()
        if alerts_df.empty:
            print("No inventory alerts triggered with default stock.")
        else:
            print("Inventory Alerts (Default Stock):\n", alerts_df)

        # Test with low initial stock and lower threshold
        print(f"\nTesting with low initial stock (20 units) and multiplier=1.0:")
        alerts_df_low_stock = generate_inventory_alerts(initial_stock=20, multiplier=1.0, first_alert_only=True)
        if alerts_df_low_stock.empty:
            print("No inventory alerts triggered with low stock.")
        else:
            print("Inventory Alerts (Low Stock Test):\n", alerts_df_low_stock)
    except Exception as e:
        print(f"Error during alert generation: {str(e)}")