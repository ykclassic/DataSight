import plotly.express as px

def correlation_heatmap(corr):

    if corr is None:
        return None

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return fig
