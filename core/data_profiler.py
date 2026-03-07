import pandas as pd

def profile_dataframe(df):

    report = []

    for col in df.columns:

        report.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": df[col].isnull().sum(),
            "missing_pct": round(df[col].isnull().mean()*100,2),
            "unique": df[col].nunique()
        })

    return pd.DataFrame(report)
