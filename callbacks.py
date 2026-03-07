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
        Output("anomaly-table", "children"),
        Input("upload-data", "contents"),
        Input("upload-data", "filename")
    )
    def process_file(contents, filename):
        # 1. Prevent update if no file is uploaded
        if contents is None:
            return "", "", {}, [], [], ""

        # 2. Parse the file
        data = parse_uploaded_file(contents, filename)
        first_table = list(data.keys())[0]
        df = data[first_table]

        # 3. Generate Analysis
        schema = analyze_schema(data)
        chart = build_chart(df)
        insights = generate_insights(df)
        recs = generate_recommendations(df)
        anomalies = detect_anomalies(df)

        # 4. Format UI Components
        preview_dt = dash_table.DataTable(
            data=df.head(10).to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            className="table"
        )

        schema_dt = dash_table.DataTable(
            data=schema.to_dict("records"),
            columns=[{"name": i, "id": i} for i in schema.columns],
            className="table"
        )
        
        anomaly_dt = dash_table.DataTable(
            data=anomalies.to_dict("records") if not anomalies.empty else [],
            columns=[{"name": i, "id": i} for i in anomalies.columns] if not anomalies.empty else [],
            className="table"
        )

        # Convert strings to Bootstrap list items
        insight_items = [html.Li(i, className="list-group-item") for i in insights]
        rec_items = [html.Li(r, className="list-group-item") for r in recs]

        # 5. Return everything in the exact order of the Outputs above
        return schema_dt, preview_dt, chart, insight_items, rec_items, anomaly_dt
