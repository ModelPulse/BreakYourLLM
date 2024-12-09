import dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.constants import (
    TABLE_CELL_STYLE,
    TABLE_DATA_CONDITIONAL_STYLE,
    TABLE_CELL_CONDITIONAL_STYLE,
    TABLE_HEADER_STYLE,
    TABLE_HEADER_CONDITIONAL_STYLE,
    TABLE_STYLE
)

def create_metadata_table(metadata_list):
    """Create the metadata table component."""
    return dash_table.DataTable(
        id='metadata-table',
        columns=[
            {'name': 'UUID', 'id': 'uuid'},
            {'name': 'Project Name', 'id': 'project_name'},
            {'name': 'Run Date', 'id': 'run_date', 'type': 'datetime'},
            {'name': 'Run By', 'id': 'run_by'},
            {'name': 'Run Time', 'id': 'run_time'},
            {'name': 'Run Duration', 'id': 'run_duration', 'type': 'numeric'},
            {'name': 'Description', 'id': 'description'},
            {'name': 'Compare', 'id': 'compare', 'type': 'text', 'presentation': 'markdown'}
        ],
        data=[{
            **row, 
            'compare': '☐'
        } for row in metadata_list],
        editable=True,
        row_selectable='single',
        sort_action='native',
        style_cell=TABLE_CELL_STYLE,
        style_data_conditional=TABLE_DATA_CONDITIONAL_STYLE,
        style_cell_conditional=TABLE_CELL_CONDITIONAL_STYLE,
        style_header=TABLE_HEADER_STYLE,
        style_header_conditional=TABLE_HEADER_CONDITIONAL_STYLE,
        style_table=TABLE_STYLE,
    )

def create_question_answer_container():
    """Create the question and answer container."""
    return dbc.Card(
        id='question-answer-container',
        style={'marginTop': '20px', 'display': 'none'},
        children=[
            dbc.CardBody([
                html.Label('Select Main Question:'),
                dcc.Dropdown(
                    id='main-question-dropdown',
                    options=[],
                    value=None
                ),

                html.Br(),

                html.Label('Select Paraphrased Question:'),
                dcc.Dropdown(
                    id='paraphrased-question-dropdown',
                    options=[],
                    value=None
                ),

                html.Br(),

                html.Div(id='table-container')
            ])
        ]
    ) 