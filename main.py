# APP VERSION v0.1-D
import streamlit as st

from streamlit_xhtml import streamlit_xhtml
# from dotenv import load_dotenv
import os

# # initialize client
# load_dotenv('./.env.txt')
aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
aws_default_region = st.secrets.AWS_DEFAULT_REGION


with open( "src/scripts/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    

# st. set_page_config(layout="wide")
# title
st.title("ArgoXai")
st.subheader("HERCULES - Contextual Financial Reviewer (Release G2)")


col1, col2, col3, c4, c5, c6, c7 ,c8 = st.columns([3,3,1,1,1,1,1,1])
company_number = col1.text_input("Enter the company number")
iterations = col2.number_input("How many review vectors?", value=1)



calculate_ratio = st.button("Start Analysis")


if calculate_ratio:  # calc ratio button pressed

    pass

