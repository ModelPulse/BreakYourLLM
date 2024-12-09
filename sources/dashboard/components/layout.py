import dash_bootstrap_components as dbc
from dash import html, dcc
from components.metrics import create_metrics_section
from components.tables import create_metadata_table, create_question_answer_container

def create_layout(metadata_list):
    """Create the main application layout."""
    return dbc.Container(
        fluid=True,
        children=[
            html.H1('LLM Test Results', style={'textAlign': 'center', 'marginTop': '20px'}),
            
            dbc.Container(
                style={'padding': '20px'},
                children=[
                    # Metrics Section
                    create_metrics_section(),
                    
                    html.Br(),
                    html.H2('Previous Test Runs'),
                    
                    # Debug info
                    html.Div(id='debug-info', children=[
                        html.P(f"Number of metadata entries: {len(metadata_list)}")
                    ]),
                    
                    # Metadata table
                    create_metadata_table(metadata_list),
                    
                    # Stores
                    dcc.Store(id='selected-file-path', storage_type='session'),
                    dcc.Store(id='unit-tests-store', storage_type='session'),
                    dcc.Store(id='selected-uuid', storage_type='session'),
                    
                    # Result displays
                    html.Div(id='file-selected-message'),
                    html.H2(id='test-results-heading'),
                    create_question_answer_container()
                ]
            )
        ]
    ) 