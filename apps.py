import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Initialize Dash with a modern Bootstrap theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

server = app.server
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=False)
