#!/bin/bash

# Configuration
LAMBDA_FUNCTION_NAME="SalesForecastFunction"
LAMBDA_ROLE_ARN="arn:aws:iam::382284572347:role/lambda-exec-role"
REGION="us-east-1"
ZIP_FILE="lambda.zip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting Lambda deployment...${NC}"

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}AWS CLI is not configured. Please run 'aws configure' first.${NC}"
    exit 1
fi

# Create zip file
echo -e "${YELLOW}Creating deployment package...${NC}"
zip -r $ZIP_FILE aws/lambda_function.py src/ model/ data/processed/cleaned_sales_data.csv

# Check if zip was created successfully
if [ ! -f "$ZIP_FILE" ]; then
    echo -e "${RED}Failed to create zip file${NC}"
    exit 1
fi

# Check if Lambda function already exists
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION &> /dev/null; then
    echo -e "${YELLOW}Updating existing Lambda function...${NC}"
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION
else
    echo -e "${YELLOW}Creating new Lambda function...${NC}"
    aws lambda create-function \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://$ZIP_FILE \
        --handler lambda_function.lambda_handler \
        --runtime python3.9 \
        --role $LAMBDA_ROLE_ARN \
        --region $REGION \
        --timeout 30 \
        --memory-size 256
fi

# Check if Lambda deployment was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Lambda function deployed successfully!${NC}"
    
    # Get Lambda function ARN
    LAMBDA_ARN=$(aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $REGION --query 'Configuration.FunctionArn' --output text)
    echo -e "${GREEN}Lambda ARN: $LAMBDA_ARN${NC}"
    
else
    echo -e "${RED}Lambda deployment failed${NC}"
    exit 1
fi

# Clean up
rm -f $ZIP_FILE
echo -e "${GREEN}Deployment package cleaned up${NC}"