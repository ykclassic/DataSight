import plotly.express as px

def build_chart(df):

    numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        fig = px.histogram(df, x=col)
        return fig

    categorical_cols = df.select_dtypes(include=["object"]).columns

    if len(categorical_cols) > 0:
        col = categorical_cols[0]
        fig = px.bar(df[col].value_counts().reset_index(),
                     x="index", y=col)
        return fig

    return None
