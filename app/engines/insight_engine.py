# app/engines/insight_engine.py
import pandas as pd
import numpy as np

def analyze_insights(db_data_dict):
    """
    db_data_dict: {
        "file1.db": {"table1": df1, "table2": df2},
        "file2.db": {"table1": df3, ...}
    }
    """
    insights = {}

    # Per file
    for filename, tables in db_data_dict.items():
        file_insights = {}
        for table_name, df in tables.items():
            numeric_df = df.select_dtypes(include=np.number)
            file_insights[table_name] = {}

            if not numeric_df.empty:
                # Detect correlations
                corr = numeric_df.corr().abs()
                high_corr = [
                    (c1, c2, corr.loc[c1, c2])
                    for c1 in corr.columns for c2 in corr.columns
                    if c1 != c2 and corr.loc[c1, c2] > 0.8
                ]
                file_insights[table_name]["high_correlations"] = high_corr

            # Detect simple trends
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]) and df[col].count() > 2:
                    # Simple trend: slope via linear regression
                    y = df[col].dropna().values
                    x = np.arange(len(y))
                    if len(y) > 1:
                        slope = np.polyfit(x, y, 1)[0]
                        if abs(slope) > 0:
                            file_insights[table_name].setdefault("trends", []).append(
                                {"column": col, "slope": float(slope)}
                            )
        insights[filename] = file_insights

    # Cross-file insights (shared columns)
    cross_file_insights = []
    all_tables = [(f, t, df) for f, tables in db_data_dict.items() for t, df in tables.items()]

    for i, (f1, t1, df1) in enumerate(all_tables):
        for j, (f2, t2, df2) in enumerate(all_tables):
            if i >= j:
                continue
            shared_cols = set(df1.columns) & set(df2.columns)
            if shared_cols:
                cross_file_insights.append({
                    "file1": f1,
                    "table1": t1,
                    "file2": f2,
                    "table2": t2,
                    "shared_columns": list(shared_cols)
                })

    insights["cross_file_relationships"] = cross_file_insights
    return insights
