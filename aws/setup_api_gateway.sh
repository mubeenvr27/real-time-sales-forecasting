#!/bin/bash

# Configuration
API_NAME="SalesForecastAPI"
LAMBDA_FUNCTION_NAME="SalesForecastFunction"
REGION="us-east-1"
STAGE_NAME="prod"

echo "Setting up API Gateway..."

# Create REST API
API_ID=$(aws apigateway create-rest-api \
  --name "$API_NAME" \
  --region $REGION \
  --query 'id' \
  --output text)

echo "API created with ID: $API_ID"

# Get the root resource ID
ROOT_RESOURCE_ID=$(aws apigateway get-resources \
  --rest-api-id $API_ID \
  --region $REGION \
  --query 'items[0].id' \
  --output text)

# Create /sales resource
SALES_RESOURCE_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_RESOURCE_ID \
  --path-part "sales" \
  --region $REGION \
  --query 'id' \
  --output text)

# Create POST method
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $SALES_RESOURCE_ID \
  --http-method POST \
  --authorization-type "NONE" \
  --region $REGION

# Get Lambda function ARN
LAMBDA_ARN=$(aws lambda get-function \
  --function-name $LAMBDA_FUNCTION_NAME \
  --region $REGION \
  --query 'Configuration.FunctionArn' \
  --output text)

# Set up Lambda integration
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $SALES_RESOURCE_ID \
  --http-method POST \
  --type AWS \
  --integration-http-method POST \
  --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations" \
  --region $REGION

# Set up method response
aws apigateway put-method-response \
  --rest-api-id $API_ID \
  --resource-id $SALES_RESOURCE_ID \
  --http-method POST \
  --status-code 200 \
  --response-models '{"application/json": "Empty"}' \
  --region $REGION

# Set up integration response
aws apigateway put-integration-response \
  --rest-api-id $API_ID \
  --resource-id $SALES_RESOURCE_ID \
  --http-method POST \
  --status-code 200 \
  --selection-pattern "" \
  --region $REGION

# Add permission for API Gateway to invoke Lambda
aws lambda add-permission \
  --function-name $LAMBDA_FUNCTION_NAME \
  --statement-id apigateway-test \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:$REGION:382284572347:$API_ID/*/POST/sales" \
  --region $REGION

# Deploy API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name $STAGE_NAME \
  --region $REGION

# Get the API URL
API_URL="https://$API_ID.execute-api.$REGION.amazonaws.com/$STAGE_NAME/sales"
echo "API Gateway setup complete!"
echo "API URL: $API_URL"
echo "Test with: curl -X POST '$API_URL' -H 'Content-Type: application/json' -d '{\"date\": \"2025-07-20\", \"sales\": 42, \"stock\": 58}'"