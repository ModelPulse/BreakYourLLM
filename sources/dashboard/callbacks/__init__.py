from .file_selection import register_file_selection_callbacks
from .graph_updates import register_graph_callbacks
from .metrics_updates import register_metrics_callbacks
from .table_updates import register_table_callbacks

def register_callbacks(app, metadata_list):
    """Register all callbacks with the app."""
    register_file_selection_callbacks(app, metadata_list)
    register_graph_callbacks(app)
    register_metrics_callbacks(app)
    register_table_callbacks(app) 