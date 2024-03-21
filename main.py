import streamlit as st
import boto3
import json

# AWS Credentials
aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
aws_default_region = st.secrets.AWS_DEFAULT_REGION

# AWS Services Clients
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)
dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)

# Streamlit UI
st.title("ArgoXai")
col1, _, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
company_number = col1.text_input("Enter CIK code")
data = st.button("Retrieve Data")

if data:
    # Ensure the CIK is a string and has leading zeros if necessary
    cik_str = company_number.zfill(10)
    
    # Retrieve s3 key from DynamoDB
    table = dynamodb.Table('sec_text')
    response = table.get_item(Key={'companyID': cik_str})
    if 'Item' in response:
        risk_factors = response['Item']['RiskFactors1A']
        # Find the latest year in the risk factors
        latest_year = max(risk_factors.keys(), key=lambda x: int(x))
        if latest_year:
            s3_key = risk_factors[latest_year]['s3key']
            bucket_name = 'argoxai-sec'
            file_path = f'txt/risk_factors/{s3_key}'
            
            # Retrieve the text file from S3
            obj = s3_client.get_object(Bucket=bucket_name, Key=file_path)
            text_data = obj['Body'].read().decode('utf-8')
            
            # Display the text file content
            st.text_area("Risk Factors", value=text_data, height=300)
        else:
            st.error("No data available for the latest year.")
    else:
        st.error("CIK code not found in the database.")



