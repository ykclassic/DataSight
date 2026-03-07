import plotly.express as px

def build_chart(df):
    """
    Renamed from correlation_heatmap to build_chart 
    to match the import in callbacks.py
    """
    if df is None or df.empty:
        return {}

    # Calculate correlation for numeric columns
    corr = df.select_dtypes(include='number').corr()
    
    if corr.empty:
        return {}

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return fig
