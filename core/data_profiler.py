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
            def dataset_health_score(profile):

    completeness = 100 - profile["missing_pct"].mean()

    consistency = 100 - (profile["unique"].mean()/100)

    integrity = 100 - (profile["missing"].sum()/100)

    score = (0.4*completeness + 0.3*consistency + 0.3*integrity)

    return round(score,2)
        })

    return pd.DataFrame(report)
