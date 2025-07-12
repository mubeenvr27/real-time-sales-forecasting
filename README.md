Real-Time Sales Forecasting & Inventory Manager

Overview
This project is a real-time sales forecasting and inventory management system designed for small retailers. Built with Python, Plotly Dash, and AWS, it provides a 7-day sales forecast, automated inventory reorder alerts, and an interactive dashboard for real-time insights. The system leverages synthetic data for rapid development and integrates with AWS for scalable deployment.
Features

7-Day Sales Forecast: Predicts future sales using time-series models (e.g., ARIMA).
Inventory Management: Generates automated reorder alerts based on stock levels.
Interactive Dashboard: Visualizes sales trends and forecasts using Plotly Dash.
Cloud Integration: Deploys forecasting and alerts via AWS Lambda and DynamoDB.
Scalable Architecture: Containerized with Docker for consistent development and deployment.

Project Structure
real-time-sales-forecasting/
├── data/
│   ├── raw/
│   │   └── sales_data.csv              # Synthetic sales data
│   └── processed/
│       └── cleaned_sales_data.csv      # Cleaned data for analysis
│       └── plots/                      # EDA visualizations
├── model/
│   └── sales_forecast.pkl              # Trained forecasting model
├── src/
│   ├── data_prep.py                    # Generates synthetic sales data
│   ├── model_train.py                  # Trains forecasting model
│   ├── predict.py                      # Generates predictions
│   ├── alert_system.py                 # Manages inventory alerts
│   └── utils.py                        # Utility functions
├── app/
│   └── dashboard.py                    # Plotly Dash dashboard
├── aws/
│   ├── lambda_function.py              # AWS Lambda handler
│   ├── deploy_lambda.sh                # Deployment script
│   └── email_template.html             # Email alert template
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker configuration
├── README.md                           # Project documentation
└── .env                                # Environment variables (not tracked)

Prerequisites

Python: Version 3.9 or higher
Docker: Version 24.0 or higher
Git: For version control
AWS Account: For cloud deployment (free-tier recommended)
VS Code or similar IDE for development

Setup Instructions

Clone the Repository:
git clone https://github.com/mubeenvr27/real-time-sales-forecasting.git
cd real-time-sales-forecasting


Set Up a Virtual Environment:
python -m venv venv


On Windows:venv\Scripts\activate


On macOS/Linux:source venv/bin/activate




Install Dependencies:
pip install -r requirements.txt


Build Docker Image:
docker build -t sales-forecasting .


Generate Synthetic Sales Data:
python src/data_prep.py


Outputs data/raw/sales_data.csv with two years of synthetic data (2023–2024).


Run EDA:
python src/data_prep.py


Generates plots in data/processed/plots/ and cleaned data in data/processed/cleaned_sales_data.csv.


Run in Docker:
docker run --rm -v $(pwd)/data:/app/data -p 8050:8050 sales-forecasting



Progress (Day 1)

Project Setup: Initialized repository, configured project structure, and set up Docker environment with Python 3.9.
Synthetic Data Generation: Created two years of synthetic sales data (2023–2024) with weekly seasonality, saved to data/raw/sales_data.csv.
Exploratory Data Analysis (EDA): Generated Plotly visualizations (daily sales trends, 7-day moving average) saved as PNGs in data/processed/plots/.
Environment Security: Secured .env file for AWS credentials and excluded data files in .gitignore.

Next Steps

Day 2: Develop and train an ARIMA model for 7-day sales forecasting in src/model_train.py.
Day 3: Implement inventory alert logic in src/alert_system.py based on stock thresholds.
Day 4: Build an interactive Plotly Dash dashboard in app/dashboard.py for real-time visualization.
Day 5: Integrate AWS Lambda and DynamoDB for cloud-based forecasting and storage.
Day 6: Add email alerts using aws/email_template.html and finalize documentation.
Day 7: Add architecture diagram, screenshots, and polish for resume-worthy presentation.

Future Enhancements

Add real-world data integration (e.g., from Kaggle or retailer APIs).
Enhance forecasting with machine learning models (e.g., Prophet, LSTM).
Include multi-user support in the Dash dashboard.
Optimize AWS costs for scalability.

Architecture Diagram
To be added upon project completion.
Screenshots
To be added after dashboard implementation.

For questions or contributions, contact mubeenvr27 or open an issue on GitHub.