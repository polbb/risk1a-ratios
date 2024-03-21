import numpy as np
import pandas as pd

import streamlit as st

def make_dataframe(results):
    df = pd.DataFrame(results)
    df.set_index('companyID', inplace=True)
    return df


def display_metrics(name, ratio, col):
    col1, col2 = st.columns([3,3])
    if col == 1:
        col1.metric(name, f"{round(ratio, 2)}")
    elif col == 2:
        col2.metric(name, f"{round(ratio, 2)}")
