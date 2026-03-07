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
    
])
