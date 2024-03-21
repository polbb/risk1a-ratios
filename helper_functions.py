import numpy as np
import pandas as pd

import streamlit as st

def make_dataframe(results):
    df = pd.DataFrame(results)
    df.set_index('companyID', inplace=True)
    return df


def display_metrics(name, ratio):
    col1, col2, col3, col4 = st.columns([3,1,1,1])
    col1.metric(name, f"{round(ratio, 2)}")
