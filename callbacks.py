from dash import Input, Output, dash_table
import pandas as pd

from core.file_loader import parse_uploaded_file
from core.schema_analyzer import analyze_schema
from core.chart_builder import build_chart
from core.anomaly_engine import detect_anomalies
from core.insight_engine import generate_insights
from core.recommendation_engine import generate_recommendations

def register_callbacks(app):

    @app.callback(
        Output("schema-table", "children"),
        Output("table-preview", "children"),
        Output("auto-chart", "figure"),
        Input("upload-data", "contents"),
        Input("upload-data", "filename")
    )
    def process_file(contents, filename):

        if contents is None:
            return "", "", {}

        data = parse_uploaded_file(contents, filename)

        schema = analyze_schema(data)

        first_table = list(data.keys())[0]
        df = data[first_table]

        preview = dash_table.DataTable(
            data=df.head(10).to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns]
        )

        chart = build_chart(df)

        schema_table = dash_table.DataTable(
            data=schema.to_dict("records"),
            columns=[{"name": i, "id": i} for i in schema.columns]
        )

        return schema_table, preview, chart
