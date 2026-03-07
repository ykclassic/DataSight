from dash import html, dcc

layout = html.Div([

    html.H1("Database Insight Explorer"),

    dcc.Upload(
        id='upload-data',
        children=html.Button("Upload Database File"),
        multiple=False
    ),

    html.Div(id="schema-table"),

    html.Div(id="table-preview"),

    dcc.Graph(id="auto-chart")
    
html.H2("Correlation Analysis"),
dcc.Graph(id="correlation-heatmap"),

html.H2("Relationships"),
dcc.Graph(id="relationship-graph"),

html.H2("Data Quality"),
html.Div(id="data-profile")

html.H2("Dataset Health Score"),
html.Div(id="health-score"),

html.H2("Insights"),
html.Ul(id="insight-list"),

html.H2("Recommendations"),
html.Ul(id="recommendation-list"),

html.H2("Detected Anomalies"),
html.Div(id="anomaly-table")
    
])
