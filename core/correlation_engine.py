import pandas as pd

def compute_correlation(df):

    numeric_df = df.select_dtypes(include=["int64","float64"])

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    return corr
