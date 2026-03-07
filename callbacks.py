from dash import Input, Output, dash_table, html
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
        Output("insight-list", "children"),
        Output("recommendation-list", "children"),
        Input("upload-data", "contents"),
        Input("upload-data", "filename")
    )
    def process_file(contents, filename):
        # Return empty values for all 5 outputs if no file is uploaded
        if contents is None:
            return "", "", {}, [], []

        # 1. Load and Analyze
        data = parse_uploaded_file(contents, filename)
        schema = analyze_schema(data)
        
        # Get the first dataframe
        first_table = list(data.keys())[0]
        df = data[first_table]

        # 2. Build UI Components
        preview = dash_table.DataTable(
            data=df.head(10).to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto'}
        )

        schema_table = dash_table.DataTable(
            data=schema.to_dict("records"),
            columns=[{"name": i, "id": i} for i in schema.columns]
        )

        # 3. Run Engines
        chart = build_chart(df)
        insights = generate_insights(df)
        recs = generate_recommendations(df)

        # Format insights/recs as list items for the html.Ul components
        insight_elements = [html.Li(ins) for ins in insights]
        rec_elements = [html.Li(rec) for rec in recs]

        # Return matches the order of the 5 Outputs above
        return schema_table, preview, chart, insight_elements, rec_elements
