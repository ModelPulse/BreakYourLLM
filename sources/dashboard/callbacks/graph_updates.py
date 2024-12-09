import json
from dash.dependencies import Input, Output, State
from dash import html, dcc
import plotly.graph_objects as go

def register_graph_callbacks(app):
    @app.callback(
        [Output('file-accuracy-graph', 'children'),
         Output('question-accuracy-graph', 'children')],
        [Input('metadata-table', 'data')]
    )
    def update_comparison_graphs(data):
        if not data:
            return "Please select files to compare.", "Please select files to compare."
        
        try:
            # Get selected files for comparison (checked boxes)
            selected_files = [row for row in data if row.get('compare') == '☒']
            
            if not selected_files:
                return "Please select files to compare.", "Please select files to compare."
            
            file_accuracies = process_file_accuracies(selected_files)
            question_accuracies = process_question_accuracies(selected_files)
            
            file_accuracy_fig = create_file_accuracy_figure(file_accuracies)
            question_accuracy_fig = create_question_accuracy_figure(question_accuracies)
            
            return [
                dcc.Graph(figure=file_accuracy_fig),
                dcc.Graph(figure=question_accuracy_fig)
            ]
            
        except Exception as e:
            print(f"Error updating comparison graphs: {e}")
            return "Error loading comparison.", "Error loading comparison."

def process_file_accuracies(selected_files):
    file_accuracies = []
    for idx, row in enumerate(selected_files):
        with open(row['file_path'], 'r') as f:
            data = json.load(f)
            for metric in data.get('metrics', []):
                if metric.get('metric_name') == 'Accuracy':
                    file_accuracies.append({
                        'File': row['uuid'][:8],
                        'Accuracy': metric.get('metric_result', 0) * 100,
                        'Index': idx
                    })
    return sorted(file_accuracies, key=lambda x: x['File'])

def process_question_accuracies(selected_files):
    question_accuracies = []
    for row in selected_files:
        with open(row['file_path'], 'r') as f:
            data = json.load(f)
            for metric in data.get('metrics', []):
                if metric.get('metric_name') == 'Accuracy':
                    question_wise = metric.get('metric_result_question_test_wise', [[]])[0]
                    question_accuracies.append({
                        'file_id': row['uuid'][:8],
                        'accuracies': [acc * 100 for acc in question_wise]
                    })
    return question_accuracies

def create_file_accuracy_figure(file_accuracies):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(len(file_accuracies))),
        y=[fa['Accuracy'] for fa in file_accuracies],
        mode='lines+markers',
        name='Accuracy',
        line=dict(color='#5cb85c', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'Accuracy Comparison Across Files ({len(file_accuracies)} files)',
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font_color='white',
        xaxis_title="File ID",
        yaxis_title="Accuracy (%)",
        yaxis_range=[0, 100],
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickangle=45,
            tickmode='array',
            ticktext=[fa['File'] for fa in file_accuracies],
            tickvals=list(range(len(file_accuracies)))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        showlegend=False
    )
    
    return fig

def create_question_accuracy_figure(question_accuracies):
    fig = go.Figure()
    
    for qa in question_accuracies:
        fig.add_trace(go.Scatter(
            x=list(range(1, len(qa['accuracies']) + 1)),
            y=qa['accuracies'],
            mode='lines+markers',
            name=qa['file_id']
        ))
    
    fig.update_layout(
        title=f'Question-wise Accuracy Comparison ({len(question_accuracies)} files)',
        xaxis_title="Question Number",
        yaxis_title="Accuracy (%)",
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font_color='white',
        yaxis_range=[0, 100],
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)'
        )
    )
    
    return fig 