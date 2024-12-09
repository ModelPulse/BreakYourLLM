from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_table
import json
from utils.constants import (
    TABLE_CELL_STYLE,
    TABLE_DATA_CONDITIONAL_STYLE,
    TABLE_CELL_CONDITIONAL_STYLE,
    TABLE_HEADER_STYLE,
    TABLE_HEADER_CONDITIONAL_STYLE,
    TABLE_STYLE
)

def register_table_callbacks(app):
    @app.callback(
        Output('metadata-table', 'data'),
        [Input('metadata-table', 'active_cell'),
         State('metadata-table', 'data')]
    )
    def toggle_checkbox(active_cell, data):
        if active_cell and active_cell['column_id'] == 'compare':
            row_idx = active_cell['row']
            data[row_idx]['compare'] = '☒' if data[row_idx]['compare'] == '☐' else '☐'
        return data

    @app.callback(
        Output('paraphrased-question-dropdown', 'options'),
        [Input('main-question-dropdown', 'value'),
         Input('unit-tests-store', 'data')]
    )
    def update_paraphrased_questions(selected_main_idx, unit_tests):
        if selected_main_idx is None or unit_tests is None:
            return []
        paraphrased_questions = unit_tests[selected_main_idx]['paraphrased_question']
        options = [{'label': pq['question'], 'value': idx} 
                  for idx, pq in enumerate(paraphrased_questions)]
        return options

    @app.callback(
        Output('table-container', 'children'),
        [Input('main-question-dropdown', 'value'),
         Input('paraphrased-question-dropdown', 'value'),
         Input('unit-tests-store', 'data')]
    )
    def update_table(selected_main_idx, selected_para_idx, unit_tests):
        if selected_main_idx is None or selected_para_idx is None or unit_tests is None:
            return html.Div()
            
        paraphrased_question = unit_tests[selected_main_idx]['paraphrased_question'][selected_para_idx]
        execution_results = paraphrased_question['execution_result']
        
        return create_results_table(execution_results)

def create_test_case_row(test_case, execution_results, test_idx):
    """Create a row for a test case with results for all answers."""
    row = {'Test Case': test_case['test_case']}
    
    for ans_idx, exec_result in enumerate(execution_results):
        test_result = exec_result['test_cases'][test_idx]
        result_text = 'True' if test_result.get('passed', False) else test_result.get('reason', 'False')
        row[f'answer_{ans_idx+1}'] = result_text
    
    return row

def create_results_table(execution_results):
    """Create the results table with execution results."""
    columns = [{'name': '', 'id': 'Test Case'}]
    data_rows = []

    # Add answer columns
    for idx, _ in enumerate(execution_results):
        columns.append({'name': f'Answer {idx+1}', 'id': f'answer_{idx+1}'})

    # Merge the 'Answer' and 'Test Results' rows
    merged_row = {'Test Case': 'Answers'}
    for idx, exec_result in enumerate(execution_results):
        merged_row[f'answer_{idx+1}'] = exec_result['answer']
    data_rows.append(merged_row)

    # Add the 'Test Cases' row
    test_cases_row = {'Test Case': 'Test Cases'}
    for idx in range(len(execution_results)):
        test_cases_row[f'answer_{idx+1}'] = ''
    data_rows.append(test_cases_row)

    # Process test cases
    test_cases = execution_results[0]['test_cases']
    for test_idx, test_case in enumerate(test_cases):
        row = create_test_case_row(test_case, execution_results, test_idx)
        data_rows.append(row)

    return create_styled_table(columns, data_rows)

def create_styled_table(columns, data_rows):
    """Create a styled DataTable component."""
    return dash_table.DataTable(
        data=data_rows,
        columns=columns,
        style_table={
            'maxHeight': '600px',
            'overflowY': 'auto',
            'overflowX': 'auto',
            'width': '100%',
            'backgroundColor': '#2b2b2b',
        },
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'pre-line',
            'height': 'auto',
            'border': '1px solid #CCCCCC',
            'backgroundColor': '#2b2b2b',
            'color': 'white',
            'padding': '10px',
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Test Case'},
             'width': '200px',
             'textAlign': 'left',
             'whiteSpace': 'pre-line',
             'minWidth': '200px',
             'maxWidth': '200px',
             'overflow': 'hidden',
             'textOverflow': 'ellipsis',
             'border': '1px solid #CCCCCC'},
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{Test Case} != "Answers" && {Test Case} != "Test Cases" && {%s} = "True"' % col['id'],
                    'column_id': col['id']
                },
                'backgroundColor': '#5cb85c',
                'color': 'white',
            } for col in columns if col['id'] != 'Test Case'
        ] + [
            {
                'if': {
                    'filter_query': '{Test Case} = "Answers"'
                },
                'backgroundColor': '#1a1a1a',
                'fontWeight': 'bold',
                'border-bottom': '2px solid white',
            },
            {
                'if': {
                    'filter_query': '{Test Case} = "Test Cases"'
                },
                'backgroundColor': '#343a40',
                'fontWeight': 'bold',
                'textAlign': 'left',
                'border-bottom': '2px solid white',
            },
        ],
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': '#1a1a1a',
            'border': '1px solid #CCCCCC',
            'color': 'white',
            'padding': '10px',
        },
        tooltip_data=[
            {
                col['id']: {
                    'value': row[col['id']] if row['Test Case'] not in ['Answers', 'Test Cases'] and row[col['id']] != 'True' else '',
                    'type': 'markdown'
                }
                for col in columns if col['id'] != 'Test Case'
            } for row in data_rows
        ],
        tooltip_duration=None,
    )