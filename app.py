import dash
print("DEBUG: Dash imported")

from layout import layout
print("DEBUG: Layout imported")

from callbacks import register_callbacks
print("DEBUG: Callbacks imported")

app = dash.Dash(__name__)
server = app.server
print("DEBUG: Server variable created")

app.layout = layout
register_callbacks(app)
print("DEBUG: App initialization complete")

if __name__ == "__main__":
    app.run(debug=True)
