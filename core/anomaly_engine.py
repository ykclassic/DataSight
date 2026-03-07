 from sklearn.ensemble import IsolationForest  # Lowercase 'from'
import pandas as pd

def detect_anomalies(df):
    # Select only numeric data for the model
    numeric_df = df.select_dtypes(include=["int64", "float64"])

    # If not enough data to find patterns, return an empty DataFrame
    if numeric_df.shape[1] < 2 or len(df) < 5:
        return pd.DataFrame()

    # Initialize and fit the model
    # contamination=0.02 means we expect roughly 2% of data to be outliers
    model = IsolationForest(contamination=0.02, random_state=42)
    
    # Generate predictions: 1 for normal, -1 for anomaly
    preds = model.fit_predict(numeric_df)

    # Add the result to a copy of the original data to avoid SettingWithCopyWarning
    df_result = df.copy()
    df_result["anomaly_score"] = preds

    # Filter for only the anomalies
    anomalies = df_result[df_result["anomaly_score"] == -1]

    return anomalies
