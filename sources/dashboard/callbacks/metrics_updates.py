import json
from dash.dependencies import Input, Output
from dash import html, dcc
import plotly.graph_objects as go

def register_metrics_callbacks(app):
    @app.callback(
        [Output('test-statistics-content', 'children'),
         Output('accuracy-chart', 'children'),
         Output('hallucination-rate', 'children'),
         Output('llm-drift-rate', 'children'),
         Output('custom-metric-1', 'children'),
         Output('custom-metric-2', 'children')],
        [Input('selected-file-path', 'data')]
    )
    def update_metrics(selected_file):
        default_values = get_default_metric_values()
        
        if selected_file is None:
            return default_values
        
        try:
            with open(selected_file, 'r') as f:
                data = json.load(f)
                metrics = data.get('metrics', [])
                
                return process_metrics(metrics)
                
        except Exception as e:
            print(f"Error loading metrics from {selected_file}: {e}")
            return default_values

def get_default_metric_values():
    """Return default values for all metrics."""
    default_stats = html.Div([
        html.P(f"Total Tests: N/A"),
        html.P(f"Test Cases: N/A"),
        html.P(f"Paraphrased: N/A"),
        html.P(f"Iterations: N/A"),
        html.P(f"Passed: N/A"),
        html.P(f"Failed: N/A")
    ])

    default_gauge = html.Div([
        html.H3("N/A", style={'textAlign': 'center', 'color': 'gray', 'marginTop': '20px'})
    ])

    default_percentage = html.Div([
        html.H3("N/A", style={'textAlign': 'center', 'color': 'gray'})
    ])

    return (
        default_stats,
        default_gauge,
        default_percentage,
        default_percentage,
        default_percentage,
        default_percentage
    )

def process_metrics(metrics):
    """Process metrics data and return formatted components."""
    statistics = get_default_metric_values()[0]  # Default value
    accuracy = get_default_metric_values()[1]    # Default value
    hallucination = get_default_metric_values()[2]  # Default value
    drift = get_default_metric_values()[3]       # Default value
    custom1 = get_default_metric_values()[4]     # Default value
    custom2 = get_default_metric_values()[5]     # Default value
    
    for metric in metrics:
        metric_name = metric.get('metric_name', '')
        
        if metric_name == 'Statistics':
            tests = metric.get('tests', {})
            statistics = html.Div([
                html.P(f"Total Tests: {tests.get('Total', 'N/A')}"),
                html.P(f"Test Cases: {tests.get('Test_cases', 'N/A')}"),
                html.P(f"Paraphrased: {tests.get('Paraphrased', 'N/A')}"),
                html.P(f"Iterations: {tests.get('Iteration', 'N/A')}"),
                html.P(f"Passed: {tests.get('Passed', 'N/A')}"),
                html.P(f"Failed: {tests.get('Failed', 'N/A')}")
            ])
        
        elif metric_name == 'Accuracy':
            accuracy_value = metric.get('metric_result', 0) * 100
            accuracy = create_accuracy_gauge(accuracy_value)
        
        elif metric_name == 'Hallucination_rate':
            hall_rate = metric.get('metric_result', 0)
            hallucination = html.Div([
                html.H3(f"{hall_rate:.1f}%", 
                       style={'textAlign': 'center', 
                             'color': '#d9534f' if hall_rate > 20 else '#5cb85c'})
            ])
        
        elif metric_name == 'LLM Drift rate':
            drift_rate = metric.get('metric_result', 0)
            drift = html.Div([
                html.H3(f"{drift_rate:.1f}%", 
                       style={'textAlign': 'center', 
                             'color': '#d9534f' if drift_rate > 30 else '#5cb85c'})
            ])
        
        elif metric_name == 'Custom metric - 1':
            custom_rate1 = metric.get('metric_result', 0)
            custom1 = html.Div([
                html.H3(f"{custom_rate1:.1f}%", 
                       style={'textAlign': 'center', 
                             'color': '#d9534f' if custom_rate1 > 50 else '#5cb85c'})
            ])
        
        elif metric_name == 'Custom metric - 2':
            custom_rate2 = metric.get('metric_result', 0)
            custom2 = html.Div([
                html.H3(f"{custom_rate2:.1f}%", 
                       style={'textAlign': 'center', 
                             'color': '#d9534f' if custom_rate2 > 50 else '#5cb85c'})
            ])
    
    return statistics, accuracy, hallucination, drift, custom1, custom2

def create_accuracy_gauge(accuracy_value):
    """Create an accuracy gauge figure."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=accuracy_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#5cb85c"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#d9534f'},
                {'range': [30, 70], 'color': '#f0ad4e'},
                {'range': [70, 100], 'color': '#5cb85c'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='#2b2b2b',
        font={'color': "white", 'family': "Arial"},
        height=200,
        margin=dict(l=30, r=30, t=30, b=0)
    )

    return html.Div([
        dcc.Graph(figure=fig, config={'displayModeBar': False})
    ]) 