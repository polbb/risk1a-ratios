import numpy as np
import pandas as pd

import streamlit as st

def make_dataframe(results):
    df = pd.DataFrame(results)
    df.set_index('companyID', inplace=True)
    return df


def display_metrics(name1, ratio1, name2, ratio2):
    col1, col2 = st.columns([3,3])

    col1.metric(name1, f"{round(ratio1, 2)}")
    col2.metric(name2, f"{round(ratio2, 2)}")
