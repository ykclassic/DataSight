import dash
from layout import layout
from callbacks import register_callbacks

# Initialize Dash
app = dash.Dash(__name__)

# Expose Flask server for Gunicorn
server = app.server

# Layout
app.layout = layout

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
