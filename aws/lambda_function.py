import sys
import os
import json
import boto3
import pandas as pd
import joblib

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Verify the src directory exists
src_path = os.path.join(project_root, 'src')
if not os.path.exists(src_path):
    raise ImportError(f"Could not find src directory at: {src_path}")

try:
    from src.predict import forecast_sales
    from src.utils import load_and_preprocess_data
    print("Successfully imported all modules")
except ImportError as e:
    print(f"Import error: {e}")
    print("Current sys.path:", sys.path)
    print("Contents of src directory:", os.listdir(src_path))
    raise



def lambda_handler(event, context):
    # Initialize AWS clients
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SalesData')
    
    # Parse incoming data (e.g., from API Gateway)
    body = json.loads(event.get('body', '{}'))
    date = body.get('date')
    sales = int(body.get('sales', 0))
    stock = int(body.get('stock', 0))
    
    # Store new data in DynamoDB
    table.put_item(
        Item={
            'date': date,
            'sales': sales,
            'stock': stock
        }
    )
    
    # Fetch historical data from DynamoDB
    response = table.scan()
    items = response['Items']
    df = pd.DataFrame(items)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').set_index('date')
    
    # Load the pre-trained model
    model_path = os.path.join(project_root, 'model', 'sales_forecast.pkl')
    model = joblib.load(model_path)
    
    # Trigger prediction
    forecast_df = forecast_sales(df)
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
        'message': 'Data stored and forecast generated',
        'forecast': forecast_df.to_dict('records')
        })
    }

if __name__ == "__main__":
    test_event = {"body": json.dumps({"date": "2025-07-15", "sales": 50, "stock": 30})}
    result = lambda_handler(test_event, None)
    print(result)