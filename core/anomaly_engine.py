from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df):

    numeric_df = df.select_dtypes(include=["int64","float64"])

    if numeric_df.shape[1] < 2:
        return None

    model = IsolationForest(contamination=0.02)

    preds = model.fit_predict(numeric_df)

    df["anomaly"] = preds

    anomalies = df[df["anomaly"] == -1]

    return anomalies
