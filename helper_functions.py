import numpy as np
import pandas as pd

import streamlit as st

def make_dataframe(results):
    df = pd.DataFrame(results)
    df.set_index('companyID', inplace=True)
    return df


def display_metrics(name1, ratio1, name2, ratio2):
    col1, col2 = st.columns([3,3])

    ratio1_display = f"{round(ratio1, 2)}" if isinstance(ratio1, (int, float)) else ratio1
    ratio2_display = f"{round(ratio2, 2)}" if isinstance(ratio2, (int, float)) else ratio2

    col1.metric(name1, ratio1_display)
    col2.metric(name2, ratio2_display)

def display_metrics_floor(name1, ratio1, name2, ratio2):
    col1, col2 = st.columns([3,3])

    ratio1_display = f"{round(ratio1, 0)}" if isinstance(ratio1, (int, float)) else ratio1
    ratio2_display = f"{round(ratio2, 0)}" if isinstance(ratio2, (int, float)) else ratio2

    col1.metric(name1, ratio1_display)
    col2.metric(name2, ratio2_display)
