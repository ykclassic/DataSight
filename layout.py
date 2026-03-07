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

])
