import dash
import dash_bootstrap_components as dbc
from components.layout import create_layout
from data.data_loader import load_metadata
from callbacks import register_callbacks

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Load metadata
metadata_list = load_metadata()

# Create layout
app.layout = create_layout(metadata_list)

# Register callbacks
register_callbacks(app, metadata_list)

if __name__ == '__main__':
    app.run_server(debug=True, port=8270) 