import json
import os
from dash.dependencies import Input, Output
from dash import html, dcc

def register_file_selection_callbacks(app, metadata_list):
    @app.callback(
        [Output('selected-file-path', 'data'),
         Output('selected-uuid', 'data'),
         Output('file-selected-message', 'children')],
        Input('metadata-table', 'selected_rows'),
        prevent_initial_call=True
    )
    def select_file(selected_rows):
        if selected_rows is None or len(selected_rows) == 0:
            return None, None, 'No file selected.'
        selected_row = selected_rows[0]
        selected_file = metadata_list[selected_row]['file_path']
        selected_uuid = metadata_list[selected_row]['uuid']
        message = f"Selected File: {os.path.basename(selected_file)}"
        return selected_file, selected_uuid, message

    @app.callback(
        [Output('main-question-dropdown', 'options'),
         Output('unit-tests-store', 'data'),
         Output('test-results-heading', 'children'),
         Output('question-answer-container', 'style')],
        [Input('selected-file-path', 'data'),
         Input('selected-uuid', 'data')]
    )
    def update_main_questions(selected_file, selected_uuid):
        if selected_file is None:
            return [], None, '', {'display': 'none'}
        try:
            with open(selected_file, 'r') as f:
                data = json.load(f)
            unit_tests = data.get('unit_tests', [])
            options = [{'label': test['question'], 'value': idx} 
                      for idx, test in enumerate(unit_tests)]
            heading = f"Test Results: {selected_uuid}"
            return options, unit_tests, heading, {'marginTop': '20px', 'display': 'block'}
        except Exception as e:
            print(f"Error loading {selected_file}: {e}")
            return [], None, '', {'display': 'none'} 