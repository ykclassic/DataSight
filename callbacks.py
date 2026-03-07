from dash import Input, Output, dash_table, html
import pandas as pd
import base64
import io

# Import your custom engines
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
        Output("correlation-heatmap", "figure"),
        Input("upload-data", "contents"),
        Input("upload-data", "filename")
    )
    def process_file(contents, filename):
        # 1. Safety check: If no file is uploaded, return empty defaults
        if contents is None:
            return "", "", {}, [], [], "", {}

        try:
            # 2. Parse the uploaded file using your core engine
            # This handles the base64 decoding internally
            data = parse_uploaded_file(contents, filename)
            
            # Extract the first available dataframe
            first_key = list(data.keys())[0]
            df = data[first_key]

            # 3. Run the analysis engines
            schema_df = analyze_schema(data)
            main_chart = build_chart(df)
            insights = generate_insights(df)
            recommendations = generate_recommendations(df)
            anomalies_df = detect_anomalies(df)

            # 4. Format Data Tables for Bootstrap display
            preview_table = dash_table.DataTable(
                data=df.head(15).to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                className="table table-hover"
            )

            schema_table = dash_table.DataTable(
                data=schema_df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in schema_df.columns],
                className="table table-sm"
            )

            # Handle anomaly table (could be empty)
            if not anomalies_df.empty:
                anomaly_display = dash_table.DataTable(
                    data=anomalies_df.head(20).to_dict("records"),
                    columns=[{"name": i, "id": i} for i in anomalies_df.columns],
                    style_header={'backgroundColor': '#f8d7da', 'color': '#721c24'},
                    className="table"
                )
            else:
                anomaly_display = html.P("No significant anomalies detected.", className="text-success p-3")

            # 5. Format Text Lists (Insights & Recommendations)
            insight_elements = [
                html.Li(ins, className="list-group-item list-group-item-action") 
                for ins in insights
            ]
            rec_elements = [
                html.Li(rec, className="list-group-item list-group-item-action border-left-primary") 
                for rec in recommendations
            ]

            # 6. Return values to the 7 defined Outputs
            # Note: We use the same 'main_chart' for both Graph slots for now
            return (
                schema_table, 
                preview_table, 
                main_chart, 
                insight_elements, 
                rec_elements, 
                anomaly_display, 
                main_chart
            )

        except Exception as e:
            # If something fails, print the error to Render logs and return error message
            print(f"ERROR processing file: {e}")
            error_msg = html.Div(f"Error processing {filename}: {str(e)}", className="alert alert-danger")
            return error_msg, error_msg, {}, [], [], error_msg, {}
