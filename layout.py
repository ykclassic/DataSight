from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col(html.H1("Database Insight Explorer", className="text-center my-4 text-primary"), width=12)
    ]),

    # Upload Section
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Data Source", className="card-title"),
                    dcc.Upload(
                        id='upload-data',
                        children=dbc.Button("Upload CSV or Excel", color="primary", className="w-100"),
                        multiple=False
                    ),
                ])
            ], className="mb-4 shadow-sm"),
            width=12
        )
    ]),

    # Main Dashboard Content
    dbc.Row([
        # Left Column: Data Preview & Schema
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Data Preview"),
                dbc.CardBody(html.Div(id="table-preview"))
            ], className="mb-4 shadow-sm"),
            
            dbc.Card([
                dbc.CardHeader("Schema Analysis"),
                dbc.CardBody(html.Div(id="schema-table"))
            ], className="shadow-sm"),
        ], lg=6, md=12),

        # Right Column: Charts & Insights
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Visual Analysis"),
                dbc.CardBody(dcc.Graph(id="auto-chart"))
            ], className="mb-4 shadow-sm"),

            dbc.Card([
                dbc.CardHeader("Automated Insights"),
                dbc.CardBody([
                    html.H6("Key Findings:", className="text-muted"),
                    html.Ul(id="insight-list", className="list-group list-group-flush"),
                    html.H6("Recommendations:", className="text-muted mt-3"),
                    html.Ul(id="recommendation-list", className="list-group list-group-flush")
                ])
            ], className="shadow-sm"),
        ], lg=6, md=12)
    ]),

    # Lower Section: Advanced Analytics
    dbc.Row([
        dbc.Col([
            html.H3("Advanced Diagnostics", className="mt-5 mb-3"),
            dbc.Tabs([
                dbc.Tab(label="Correlation", children=[
                    dbc.Card(dbc.CardBody(dcc.Graph(id="correlation-heatmap")), className="border-top-0 shadow-sm")
                ]),
                dbc.Tab(label="Anomalies", children=[
                    dbc.Card(dbc.CardBody(html.Div(id="anomaly-table")), className="border-top-0 shadow-sm")
                ]),
                dbc.Tab(label="Data Quality", children=[
                    dbc.Card(dbc.CardBody(html.Div(id="data-profile")), className="border-top-0 shadow-sm")
                ]),
            ])
        ], width=12)
    ], className="mb-5")
], fluid=True)
