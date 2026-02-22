# app/engines/insight_engine.py
import pandas as pd
import numpy as np


def analyze_insights(db_data_dict):
    insights = {}

    for filename, tables in db_data_dict.items():
        file_insights = {}

        for table_name, df in tables.items():
            file_insights[table_name] = {}

            try:
                numeric_df = df.select_dtypes(include=np.number)

                # Correlations
                if not numeric_df.empty and numeric_df.shape[1] > 1:
                    corr = numeric_df.corr().abs()
                    high_corr = [
                        (c1, c2, float(corr.loc[c1, c2]))
                        for c1 in corr.columns
                        for c2 in corr.columns
                        if c1 != c2 and corr.loc[c1, c2] > 0.8
                    ]
                    file_insights[table_name][
                        "high_correlations"
                    ] = high_corr

                # Predictive trend slopes
                trends = []
                for col in numeric_df.columns:
                    y = df[col].dropna().values
                    if len(y) > 1:
                        x = np.arange(len(y))
                        slope = float(np.polyfit(x, y, 1)[0])
                        trends.append({"column": col, "slope": slope})
                if trends:
                    file_insights[table_name]["trends"] = trends

            except Exception as e:
                file_insights[table_name]["error"] = str(e)

        insights[filename] = file_insights

    # Cross-file shared columns
    cross_file = []
    all_tables = [
        (f, t, df)
        for f, tables in db_data_dict.items()
        for t, df in tables.items()
    ]

    for i, (f1, t1, df1) in enumerate(all_tables):
        for j, (f2, t2, df2) in enumerate(all_tables):
            if i >= j:
                continue
            shared = set(df1.columns) & set(df2.columns)
            if shared:
                cross_file.append(
                    {
                        "file1": f1,
                        "table1": t1,
                        "file2": f2,
                        "table2": t2,
                        "shared_columns": list(shared),
                    }
                )

    insights["cross_file_relationships"] = cross_file
    return insights
