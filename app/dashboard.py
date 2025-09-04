import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table
import sys
import os
from flask import Flask, Response

# Add src/ to the module search path before imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import load_and_preprocess_data after updating path
from utils import load_and_preprocess_data


# Initialize Flask server and Dash app
server = Flask(__name__)
app = Dash(__name__, server=server)


# Load data with error handling
def load_data():
    try:
        historical_df = load_and_preprocess_data()
        if 'sales' not in historical_df.columns or 'stock' not in historical_df.columns:
            raise ValueError("Historical data must contain 'sales' and 'stock' columns")
    except Exception as e:
        print(f"Error loading historical data: {str(e)}")
        historical_df = pd.DataFrame({'sales': [], 'stock': []}, index=pd.DatetimeIndex([]))

    try:
        forecast_df = pd.read_csv('data/processed/forecasted_sales.csv')
        forecast_df['date'] = pd.to_datetime(forecast_df['date'], errors='coerce')
        if 'forecasted_sales' not in forecast_df.columns or forecast_df['date'].isna().any():
            raise ValueError("Forecast data must contain valid 'date' and 'forecasted_sales' columns")
    except Exception as e:
        print(f"Error loading forecast data: {str(e)}")
        forecast_df = pd.DataFrame({'date': [], 'forecasted_sales': []})

    try:
        alerts_df = pd.read_csv('data/processed/inventory_alerts.csv')
        alerts_df['date'] = pd.to_datetime(alerts_df['date'], errors='coerce')
        if not {'date', 'stock', 'forecasted_sales', 'message'}.issubset(alerts_df.columns):
            raise ValueError("Alerts data must contain 'date', 'stock', 'forecasted_sales', 'message' columns")
    except Exception as e:
        print(f"Error loading alerts data: {str(e)}")
        alerts_df = pd.DataFrame({'date': [], 'stock': [], 'forecasted_sales': [], 'message': []})

    return historical_df, forecast_df, alerts_df


# Load data
historical_df, forecast_df, alerts_df = load_data()



# Create sales plot
fig_sales = go.Figure()
fig_sales.add_trace(go.Scatter(x=historical_df.index, y=historical_df['sales'], name='Historical Sales', line=dict(color='#1f77b4')))
if not forecast_df.empty:
    fig_sales.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['forecasted_sales'], name='Forecasted Sales', line=dict(dash='dash', color='#ff7f0e')))
fig_sales.update_layout(
    title='Sales Trend and Forecast (2025)',
    xaxis_title='Date',
    yaxis_title='Sales (Units)',
    template='plotly_dark',
    margin=dict(l=50, r=50, t=50, b=50)
)



# Create forecast table
forecast_table_data = forecast_df[['date', 'forecasted_sales']].copy()
forecast_table_data['date'] = forecast_table_data['date'].dt.strftime('%Y-%m-%d')
if not forecast_df.empty:
    current_stock = historical_df['stock'].iloc[-1] if not historical_df.empty else 60
    stock_after_sales = current_stock - forecast_df['forecasted_sales'].cumsum()
    forecast_table_data['stock_after_sales'] = stock_after_sales.clip(lower=0)  # Cap stock at 0
else:
    forecast_table_data['stock_after_sales'] = []




# Create alerts table
alerts_table_data = alerts_df[['date', 'stock', 'forecasted_sales', 'message']].copy()
alerts_table_data['date'] = alerts_table_data['date'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if pd.notna(x) else '')

# Health check endpoint
@server.route('/healthz')
def health_check():
    return Response("OK", status=200)

# Define layout
app.layout = html.Div([
    html.H1("Real-Time Sales Forecasting & Inventory Manager", style={'textAlign': 'center', 'color': '#ffffff'}),
    html.H2("Sales Trend", style={'color': '#ffffff'}),
    dcc.Graph(figure=fig_sales),
    html.H2("Forecasted Stock Needs", style={'color': '#ffffff'}),
    dash_table.DataTable(
        data=forecast_table_data.to_dict('records'),
        columns=[
            {'name': 'Date', 'id': 'date'},
            {'name': 'Forecasted Sales (Units)', 'id': 'forecasted_sales'},
            {'name': 'Stock After Sales (Units)', 'id': 'stock_after_sales'}
        ],
        style_table={'overflowX': 'auto', 'backgroundColor': '#2b2b2b'},
        style_cell={'textAlign': 'left', 'color': '#ffffff', 'backgroundColor': '#2b2b2b'},
        style_header={'backgroundColor': '#1f77b4', 'fontWeight': 'bold', 'color': '#ffffff'}
    ),
    html.H2("Inventory Alerts", style={'color': '#ffffff'}),
    dash_table.DataTable(
        data=alerts_table_data.to_dict('records'),
        columns=[
            {'name': 'Date', 'id': 'date'},
            {'name': 'Stock Level (Units)', 'id': 'stock'},
            {'name': 'Forecasted Sales (Units)', 'id': 'forecasted_sales'},
            {'name': 'Alert Message', 'id': 'message'}
        ],
        style_table={'overflowX': 'auto', 'backgroundColor': '#2b2b2b'},
        style_cell={'textAlign': 'left', 'color': '#ffffff', 'backgroundColor': '#2b2b2b'},
        style_header={'backgroundColor': '#ff7f0e', 'fontWeight': 'bold', 'color': '#ffffff'}
    )
], style={'backgroundColor': '#1a1a1a', 'padding': '20px'})

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 8050))  # Use PORT env var from Render, default to 8050 locally
    app.run(debug=True, host='0.0.0.0', port=port)



    