import sys
import os
import json
import boto3
import pandas as pd

# Set correct paths for Lambda environment
sys.path.insert(0, '/var/task')
sys.path.insert(0, '/var/task/src')

try:
    from src.predict import forecast_sales
    print("Successfully imported forecast_sales")
except ImportError as e:
    print(f"Import error: {e}")
    # Try alternative import paths
    try:
        from predict import forecast_sales
        print("Successfully imported with alternative path")
    except ImportError as e2:
        print(f"Alternative import error: {e2}")
        raise

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
        # Parse the incoming event
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        # Extract data
        date = body.get('date')
        sales = int(body.get('sales', 0))
        stock = int(body.get('stock', 0))

        if not all([date, sales, stock]):
            return {
                'statusCode': 400, 
                'body': json.dumps({'error': 'Missing required fields: date, sales, stock'})
            }

        # Initialize DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('SalesData')

        # Store in DynamoDB
        table.put_item(
            Item={
                'date': date,
                'sales': sales,
                'stock': stock
            }
        )
        print(f"Data stored: {date}, sales: {sales}, stock: {stock}")

        # Get all data for forecasting
        response = table.scan()
        items = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        
        # Convert to DataFrame and prepare for forecasting
        df = pd.DataFrame(items)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Set date as index (required by forecast_sales function)
        df_for_forecast = df.set_index('date')
        
        # Generate forecast - forecast_sales loads the model internally
        try:
            forecast_df = forecast_sales(df_for_forecast)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Data stored and forecast generated',
                    'forecast': forecast_df.to_dict('records')
                })
            }
            
        except Exception as e:
            print(f"Forecast error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Data stored successfully but forecast failed',
                    'error': str(e)
                })
            }
            
    except Exception as e:
        print(f"Lambda error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Test function
if __name__ == "__main__":
    test_event = {
        "body": json.dumps({
            "date": "2025-07-15", 
            "sales": 50, 
            "stock": 30
        })
    }
    result = lambda_handler(test_event, None)
    print("Test result:", result)