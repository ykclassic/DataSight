def analyze_schema(db_data):

    schema_summary = {}

    for table_name, df in db_data.items():

        columns = {}

        for col in df.columns:
            columns[col] = {
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "unique_values": int(df[col].nunique())
            }

        schema_summary[table_name] = columns

    return schema_summary
