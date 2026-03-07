import pandas as pd

def analyze_schema(dataframes):

    schema = []

    for table, df in dataframes.items():

        for column in df.columns:
            schema.append({
                "table": table,
                "column": column,
                "dtype": str(df[column].dtype),
                "nulls": df[column].isnull().sum(),
                "unique": df[column].nunique()
            })

    return pd.DataFrame(schema)
