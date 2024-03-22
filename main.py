import streamlit as st
import boto3
from helper_functions import display_metrics, display_metrics_floor


# Streamlit UI
st.set_page_config(layout="wide")  # Force wide mode
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# AWS Credentials
aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
aws_default_region = st.secrets.AWS_DEFAULT_REGION

# AWS Services Clients
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)
dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)



st.title("ArgoXai")
col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
company_number = col1.text_input("Enter CIK code")
data = st.button("Retrieve Data")

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
            st.text_area("Risk Factors", value=text_data, height=500)
        else:
            st.error("No data available for the latest year.")
    else:
        st.error("CIK code not found in the database.")

    # Retrieve financial ratios from DynamoDB
    ratios_table = dynamodb.Table('sec_ratios')
    ratios_response = ratios_table.get_item(Key={'companyID': cik_str, 'year': latest_year})
    if 'Item' in ratios_response:
        # Retrieve data for calculations
        def parse_int(value):
            try:
                return int(value)
            except ValueError:
                return 'N/A'

        current_assets_latest = parse_int(ratios_response['Item'].get('current_assets', [{}])[0].get('value', 'N/A'))
        creditors_latest = parse_int(ratios_response['Item'].get('creditors', [{}])[0].get('value', 'N/A'))
        inventory_prepaid_expenses_latest = parse_int(ratios_response['Item'].get('inventory_prepaid_expenses', [{}])[0].get('value', 'N/A'))
        cost_of_sales_latest = parse_int(ratios_response['Item'].get('cost_of_sales', [{}])[0].get('value', 'N/A'))
        stocks_latest = parse_int(ratios_response['Item'].get('stocks', [{}])[0].get('value', 'N/A'))
        total_assets_latest = parse_int(ratios_response['Item'].get('total_assets', [{}])[0].get('value', 'N/A'))
        cash_and_cash_equivalents_latest = parse_int(ratios_response['Item'].get('cash_and_cash_equivalents', [{}])[0].get('value', 'N/A'))

        current_assets_previous = parse_int(ratios_response['Item'].get('current_assets', [{}])[1].get('value', 'N/A'))
        creditors_previous = parse_int(ratios_response['Item'].get('creditors', [{}])[1].get('value', 'N/A'))
        inventory_prepaid_expenses_previous = parse_int(ratios_response['Item'].get('inventory_prepaid_expenses', [{}])[1].get('value', 'N/A'))
        cost_of_sales_previous = parse_int(ratios_response['Item'].get('cost_of_sales', [{}])[1].get('value', 'N/A'))
        stocks_previous = parse_int(ratios_response['Item'].get('stocks', [{}])[1].get('value', 'N/A'))
        total_assets_previous = parse_int(ratios_response['Item'].get('total_assets', [{}])[1].get('value', 'N/A'))
        cash_and_cash_equivalents_previous = parse_int(ratios_response['Item'].get('cash_and_cash_equivalents', [{}])[1].get('value', 'N/A'))

        # Calculate ratios for latest and previous year
        wc_ratio_latest = current_assets_latest / creditors_latest if 'N/A' not in [current_assets_latest, creditors_latest] else 'N/A'
        quick_ratio_latest = (current_assets_latest - inventory_prepaid_expenses_latest) / creditors_latest if 'N/A' not in [current_assets_latest, inventory_prepaid_expenses_latest, creditors_latest] else 'N/A'
        itr_ratio_latest = cost_of_sales_latest / stocks_latest if 'N/A' not in [cost_of_sales_latest, stocks_latest] else 'N/A'
        wr_score_latest = (current_assets_latest / total_assets_latest) / (creditors_latest / total_assets_latest) if 'N/A' not in [current_assets_latest, total_assets_latest, creditors_latest] else 'N/A'
        gap_index_latest = (itr_ratio_latest / wr_score_latest) * 100 if 'N/A' not in [itr_ratio_latest, wr_score_latest] else 'N/A'
        cash_ratio_latest = cash_and_cash_equivalents_latest / creditors_latest if 'N/A' not in [cash_and_cash_equivalents_latest, creditors_latest] else 'N/A'

        wc_ratio_previous = current_assets_previous / creditors_previous if 'N/A' not in [current_assets_previous, creditors_previous] else 'N/A'
        quick_ratio_previous = (current_assets_previous - inventory_prepaid_expenses_previous) / creditors_previous if 'N/A' not in [current_assets_previous, inventory_prepaid_expenses_previous, creditors_previous] else 'N/A'
        itr_ratio_previous = cost_of_sales_previous / stocks_previous if 'N/A' not in [cost_of_sales_previous, stocks_previous] else 'N/A'
        wr_score_previous = (current_assets_previous / total_assets_previous) / (creditors_previous / total_assets_previous) if 'N/A' not in [current_assets_previous, total_assets_previous, creditors_previous] else 'N/A'
        gap_index_previous = (itr_ratio_previous / wr_score_previous) * 100 if 'N/A' not in [itr_ratio_previous, wr_score_previous] else 'N/A'
        cash_ratio_previous = cash_and_cash_equivalents_previous / creditors_previous if 'N/A' not in [cash_and_cash_equivalents_previous, creditors_previous] else 'N/A'

        with st.container(border=True):
            c1, c2, c3, c4, c5, c6 = st.columns([1,1,1,1,1,1])

            with c1.container(border=True):
                st.header('WC Ratio')
                display_metrics('WC Latest', wc_ratio_latest, 'WC Previous', wc_ratio_previous)
            with c2.container(border=True):
                st.header('Quick Ratio')
                display_metrics('Quick Latest', quick_ratio_latest, 'Quick Previous', quick_ratio_previous)
            with c3.container(border=True):
                st.header('ITR Ratio')
                display_metrics('ITR Latest', itr_ratio_latest, 'ITR Previous', itr_ratio_previous)
            with c4.container(border=True):
                st.header('WR Score')
                display_metrics('WR Latest', wr_score_latest, 'WR Previous', wr_score_previous)
            with c5.container(border=True):
                st.header('GAP Index')
                display_metrics_floor('GAP Latest', gap_index_latest, 'GAP Previous', gap_index_previous)
            with c6.container(border=True):
                st.header('Cash Ratio')
                display_metrics('Cash Latest', cash_ratio_latest, 'Cash Previous', cash_ratio_previous)

    else:
        st.error("Financial ratios not found in the database.")


