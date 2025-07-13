# Real-Time Sales Forecasting & Inventory Manager

## Overview
A real-time sales forecasting and inventory management system for small retailers, built with Python, Plotly Dash, and AWS. Features include a 7-day sales forecast, automated reorder alerts, and a live dashboard.

## Project Structure
```
real-time-sales-forecasting/
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   └── processed/
│       └── cleaned_sales_data.csv
│       └── forecasted_sales.csv
├── model/
│   └── sales_forecast.pkl
├── src/
│   ├── data_prep.py
│   ├── model_train.py
│   ├── predict.py
│   ├── alert_system.py
│   └── utils.py
├── app/
│   └── dashboard.py
├── aws/
│   ├── lambda_function.py
│   ├── deploy_lambda.sh
│   └── email_template.html
├── requirements.txt
├── Dockerfile
├── README.md
└── .env
```

## Setup Instructions
1. Clone the repository.
2. Set up a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Build Docker image: `docker build -t sales-forecasting .`
5. Run data preparation: `python src/data_prep.py`
6. Train model: `python src/model_train.py`
7. Generate forecast: `python src/predict.py`
8. Generate inventory alerts: `python src/alert_system.py`

## Progress
- **Day 1**:
  - Set up project structure and Docker environment.
  - Generated synthetic sales data for 180 days.
  - Performed EDA with Plotly visualizations to identify sales trends.
- **Day 2**:
  - Preprocessed sales data for time series modeling.
  - Trained an ARIMA model using statsmodels for 7-day sales forecasting.
  - Saved the model and generated forecasts, stored in `data/processed/forecasted_sales.csv`.

- **Day 3**:
  - Implemented inventory alert logic to detect low stock based on forecasted sales.
  - Defined reorder threshold as 1.5 * average daily sales.
  - Generated alert messages saved to `data/processed/inventory_alerts.csv`.


## Next Steps
- Day 4: Develop a Plotly Dash dashboard.
- Day 5: Integrate AWS Lambda and DynamoDB.
- Day 6: Add email alerts and finalize documentation.

*Architecture diagram and screenshots to be added later.*