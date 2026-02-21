import numpy as np

def profile_tables(db_data):

    profile_results = {}

    for table_name, df in db_data.items():

        numeric_df = df.select_dtypes(include=np.number)

        if not numeric_df.empty:
            correlation = numeric_df.corr().to_dict()
            stats = numeric_df.describe().to_dict()
        else:
            correlation = {}
            stats = {}

        profile_results[table_name] = {
            "statistics": stats,
            "correlation": correlation
        }

    return profile_results
