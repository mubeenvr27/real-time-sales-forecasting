import boto3
from botocore.exceptions import ClientError
import pandas as pd

def create_sales_table():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    try:
        response = dynamodb.create_table(
            TableName='SalesData',
            KeySchema=[
                {'AttributeName': 'date', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'date', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully:", response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            raise e

def populate_sales_table(file_path='data/processed/cleaned_sales_data.csv'):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('SalesData')
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    print(f"Data loaded, rows: {len(df)}")
    
    success_count = 0
    for index, row in df.iterrows():
        try:
            table.put_item(
                Item={
                    'date': row['date'].strftime('%Y-%m-%d'),
                    'sales': int(row['sales']),
                    'stock': int(row['stock'])
                }
            )
            success_count += 1
            if index % 100 == 0:  # Progress update every 100 rows
                print(f"Processed {index + 1} rows, {success_count} successes")
        except ClientError as e:
            print(f"Error at row {index}: {e}")
    print(f"Data population complete: {success_count} rows inserted successfully.")

if __name__ == "__main__":
    create_sales_table()
    populate_sales_table()