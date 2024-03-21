import streamlit as st
import boto3
from helper_functions import display_metrics
import json

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# AWS Credentials
aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
aws_default_region = st.secrets.AWS_DEFAULT_REGION

# AWS Services Clients
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)
dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)

# Streamlit UI
st.title("ArgoXai")
col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
company_number = col1.text_input("Enter CIK code")
data = col2.button("Retrieve Data")

if data:
    # Ensure the CIK is a string and has leading zeros if necessary
    cik_str = company_number.zfill(10)
    
    # Retrieve s3 key from DynamoDB for Risk Factors
    table = dynamodb.Table('sec_text')
    response = table.get_item(Key={'companyID': cik_str})
    if 'Item' in response:
        risk_factors = response['Item']['RiskFactors1A']
        # Find the latest year in the risk factors
        latest_year = max(risk_factors.keys(), key=lambda x: int(x))
        if latest_year:
            s3_key = risk_factors[latest_year]['s3key']
            bucket_name = 'argoxai-sec'
            
            # Retrieve the text file from S3 for Risk Factors
            obj = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
            text_data = obj['Body'].read().decode('utf-8')
            
            # Display the text file content for Risk Factors
            st.text_area("Risk Factors", value=text_data, height=600)
        else:
            st.error("No data available for the latest year.")
    else:
        st.error("CIK code not found in the database.")

    # Retrieve financial ratios from DynamoDB
    ratios_table = dynamodb.Table('sec_ratios')
    ratios_response = ratios_table.get_item(Key={'companyID': cik_str, 'year': latest_year})
    if 'Item' in ratios_response:
        cost_of_sales_data_latest = int(ratios_response['Item'].get('cost_of_sales', [{}])[0].get('value', 'N/A'))
        stocks_data_latest = int(ratios_response['Item'].get('stocks', [{}])[0].get('value', 'N/A'))
        cost_of_sales_data_previous = int(ratios_response['Item'].get('cost_of_sales', [{}])[1].get('value', 'N/A'))
        stocks_data_previous = int(ratios_response['Item'].get('stocks', [{}])[1].get('value', 'N/A'))
        
        if cost_of_sales_data_latest != 'N/A' and stocks_data_latest != 'N/A' and cost_of_sales_data_previous != 'N/A' and stocks_data_previous != 'N/A':
            # Calculate ITR Ratio for latest and previous year
            itr_ratio_latest = cost_of_sales_data_latest / stocks_data_latest
            itr_ratio_previous = cost_of_sales_data_previous / stocks_data_previous

            with st.container(border=True):
                st.header('ITR Ratio')
                display_metrics('ITR Latest Year', itr_ratio_latest, 'ITR Previous Year', itr_ratio_previous)
        else:
            st.error("Cost of Sales or Stocks data is not available for one or both years.")
    else:
        st.error("Financial ratios not found in the database.")

