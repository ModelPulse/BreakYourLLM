from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


def create_metrics_section():
    """Create the metrics cards section."""
    return html.Div([
        # Metrics Row
        dbc.Row([
            # Test Statistics
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Test Statistics"),
                    dbc.CardBody(id='test-statistics-content')
                ])
            ], width=3),
            
            # Accuracy Chart
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Accuracy"),
                    dbc.CardBody(id='accuracy-chart')
                ])
            ], width=3),
            
            # Right side column group
            dbc.Col([
                # First row - Hallucination and Drift
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Hallucination Rate"),
                            dbc.CardBody(id='hallucination-rate')
                        ])
                    ], width=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("LLM Drift Rate"),
                            dbc.CardBody(id='llm-drift-rate')
                        ])
                    ], width=6),
                ], className='mb-3'),
                
                # Second row - Custom Metrics
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Custom Metric 1"),
                            dbc.CardBody(id='custom-metric-1')
                        ])
                    ], width=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Custom Metric 2"),
                            dbc.CardBody(id='custom-metric-2')
                        ])
                    ], width=6),
                ]),
            ], width=6),
        ], className='mb-4'),

        # Graphs Row
        dbc.Row([
            # Graph 1 - File Accuracy Comparison
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("File Accuracy Comparison"),
                    dbc.CardBody(id='file-accuracy-graph')
                ])
            ], width=6),
            
            # Graph 2 - Question-wise Accuracy
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Question-wise Accuracy"),
                    dbc.CardBody(id='question-accuracy-graph')
                ])
            ], width=6),
        ], className='mb-4'),
    ])