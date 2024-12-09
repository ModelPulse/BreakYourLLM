# Table Styles
TABLE_CELL_STYLE = {
    'textAlign': 'left',
    'whiteSpace': 'normal',
    'height': 'auto',
    'backgroundColor': '#2b2b2b',
    'color': 'white',
}

TABLE_DATA_CONDITIONAL_STYLE = [
    {
        'if': {'column_id': 'compare'},
        'cursor': 'pointer',
        'textAlign': 'center'
    }
]

TABLE_CELL_CONDITIONAL_STYLE = [
    {
        'if': {'column_id': 'uuid'},
        'width': '325px',
        'minWidth': '300px',
        'maxWidth': '400px',
        'whiteSpace': 'normal',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    {
        'if': {'column_id': 'description'},
        'width': '325px',
        'minWidth': '300px',
        'maxWidth': '350px',
        'whiteSpace': 'normal',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
]

TABLE_HEADER_STYLE = {
    'fontWeight': 'bold',
    'backgroundColor': '#1a1a1a',
    'color': 'white',
}

TABLE_HEADER_CONDITIONAL_STYLE = [
    {
        'if': {'column_id': column_id},
        'pointer-events': 'none',
        'cursor': 'default',
        'textDecoration': 'none',
    } for column_id in ['uuid', 'run_time', 'description']
]

TABLE_STYLE = {
    'maxHeight': '400px',
    'overflowY': 'auto',
    'width': '100%',
} 