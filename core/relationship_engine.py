import pandas as pd

def detect_relationships(dataframes):

    relationships = []

    tables = list(dataframes.keys())

    for i in range(len(tables)):
        for j in range(i+1, len(tables)):

            df1 = dataframes[tables[i]]
            df2 = dataframes[tables[j]]

            common_cols = set(df1.columns).intersection(df2.columns)

            for col in common_cols:
                relationships.append({
                    "table_1": tables[i],
                    "table_2": tables[j],
                    "column": col
                })

    return pd.DataFrame(relationships)
