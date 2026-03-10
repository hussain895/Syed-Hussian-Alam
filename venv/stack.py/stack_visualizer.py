"""
Interactive Stack Visualizer using Dash and Plotly
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
from stack import Stack

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize a global stack for the visualizer
global_stack = Stack(max_size=10)

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("Stack Visualizer", style={"textAlign": "center", "color": "#2c3e50", "marginBottom": 30}),
        
        html.Div([
            # Input section
            html.Div([
                html.Label("Enter Value:", style={"fontWeight": "bold"}),
                dcc.Input(
                    id="input-value",
                    type="number",
                    placeholder="Enter a number",
                    style={
                        "padding": "10px",
                        "marginRight": "10px",
                        "borderRadius": "5px",
                        "border": "1px solid #bdc3c7",
                        "width": "150px"
                    }
                ),
                html.Button(
                    "Push",
                    id="push-btn",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "marginRight": "10px",
                        "backgroundColor": "#27ae60",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontWeight": "bold"
                    }
                ),
                html.Button(
                    "Pop",
                    id="pop-btn",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "marginRight": "10px",
                        "backgroundColor": "#e74c3c",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontWeight": "bold"
                    }
                ),
                html.Button(
                    "Clear",
                    id="clear-btn",
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "backgroundColor": "#95a5a6",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontWeight": "bold"
                    }
                ),
            ], style={
                "padding": "20px",
                "backgroundColor": "#ecf0f1",
                "borderRadius": "10px",
                "marginBottom": "20px"
            }),
            
            # Status section
            html.Div([
                html.Div([
                    html.Span("Stack Size: ", style={"fontWeight": "bold"}),
                    html.Span(id="stack-size", style={"fontSize": "18px", "color": "#3498db"}),
                ], style={"marginRight": "30px"}),
                html.Div([
                    html.Span("Top Element: ", style={"fontWeight": "bold"}),
                    html.Span(id="top-element", style={"fontSize": "18px", "color": "#9b59b6"}),
                ]),
            ], style={
                "padding": "15px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "10px",
                "display": "flex",
                "marginBottom": "20px"
            }),
            
            # Message section
            html.Div(id="message-display", style={
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "5px",
                "textAlign": "center",
                "fontWeight": "bold",
                "minHeight": "20px"
            }),
        ], style={"maxWidth": "800px", "margin": "0 auto"}),
        
        # Visualization section
        html.Div([
            dcc.Graph(id="stack-visualization"),
        ], style={
            "marginTop": "30px",
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
        }),
        
        # Information section
        html.Div([
            html.H3("Stack Operations", style={"color": "#2c3e50"}),
            html.Ul([
                html.Li("Push: Add an element to the top of the stack"),
                html.Li("Pop: Remove the top element from the stack"),
                html.Li("Peek: View the top element (displayed above)"),
                html.Li("Clear: Remove all elements from the stack"),
            ], style={"lineHeight": "1.8"})
        ], style={
            "marginTop": "30px",
            "padding": "20px",
            "backgroundColor": "#ecf0f1",
            "borderRadius": "10px",
            "maxWidth": "800px",
            "margin": "30px auto"
        }),
    ], style={
        "padding": "30px",
        "backgroundColor": "#f5f5f5",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif"
    })
], style={"margin": 0, "padding": 0})


@callback(
    [Output("stack-visualization", "figure"),
     Output("stack-size", "children"),
     Output("top-element", "children"),
     Output("message-display", "children"),
     Output("message-display", "style"),
     Output("input-value", "value")],
    [Input("push-btn", "n_clicks"),
     Input("pop-btn", "n_clicks"),
     Input("clear-btn", "n_clicks")],
    [State("input-value", "value")],
    prevent_initial_call=False
)
def update_stack(push_clicks, pop_clicks, clear_clicks, input_value):
    """Callback to handle stack operations and update visualization."""
    
    # Determine which button was clicked
    ctx = dash.callback_context
    
    message = ""
    message_style = {
        "padding": "10px",
        "marginBottom": "20px",
        "borderRadius": "5px",
        "textAlign": "center",
        "fontWeight": "bold",
        "minHeight": "20px"
    }
    
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == "push-btn":
            if input_value is not None:
                try:
                    global_stack.push(int(input_value))
                    message = f"✓ Pushed {int(input_value)} to the stack"
                    message_style["backgroundColor"] = "#d4edda"
                    message_style["color"] = "#155724"
                except OverflowError:
                    message = "✗ Stack is full! Cannot push more elements."
                    message_style["backgroundColor"] = "#f8d7da"
                    message_style["color"] = "#721c24"
            else:
                message = "✗ Please enter a value first"
                message_style["backgroundColor"] = "#f8d7da"
                message_style["color"] = "#721c24"
        
        elif button_id == "pop-btn":
            if not global_stack.is_empty():
                popped = global_stack.pop()
                message = f"✓ Popped {popped} from the stack"
                message_style["backgroundColor"] = "#d4edda"
                message_style["color"] = "#155724"
            else:
                message = "✗ Stack is empty! Cannot pop."
                message_style["backgroundColor"] = "#f8d7da"
                message_style["color"] = "#721c24"
        
        elif button_id == "clear-btn":
            global_stack.items.clear()
            message = "✓ Stack cleared"
            message_style["backgroundColor"] = "#d4edda"
            message_style["color"] = "#155724"
    
    # Generate visualization
    fig = create_stack_visualization(global_stack)
    
    # Get stack size and top element
    stack_size = global_stack.size()
    top_element = str(global_stack.peek()) if not global_stack.is_empty() else "Empty"
    
    return fig, stack_size, top_element, message, message_style, None


def create_stack_visualization(stack):
    """Create a visualization of the stack."""
    
    if stack.is_empty():
        # Empty stack visualization
        fig = go.Figure()
        fig.add_shape(
            type="rect",
            x0=1, y0=0, x1=3, y1=5,
            line=dict(color="gray", width=2),
            fillcolor="lightgray",
            opacity=0.5
        )
        fig.add_annotation(
            x=2, y=2.5,
            text="Stack is Empty",
            font=dict(size=20, color="gray"),
            showarrow=False
        )
        fig.update_layout(
            title="Stack Visualization (Empty)",
            xaxis_range=[0, 4],
            yaxis_range=[-1, 6],
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=500,
            showlegend=False
        )
        return fig
    
    # Create stack blocks
    items = stack.items
    num_items = len(items)
    
    fig = go.Figure()
    
    # Draw stack blocks
    colors = px.colors.qualitative.Set3
    
    for i, item in enumerate(items):
        y_pos = i
        color = colors[i % len(colors)]
        
        # Draw rectangle for each item
        fig.add_shape(
            type="rect",
            x0=1, y0=y_pos, x1=3, y1=y_pos + 0.9,
            line=dict(color="#2c3e50", width=2),
            fillcolor=color,
        )
        
        # Add text label
        fig.add_annotation(
            x=2, y=y_pos + 0.45,
            text=str(item),
            font=dict(size=16, color="#2c3e50", family="Arial Black"),
            showarrow=False
        )
        
        # Add position label
        if i == num_items - 1:
            fig.add_annotation(
                x=3.5, y=y_pos + 0.45,
                text="← TOP",
                font=dict(size=12, color="#e74c3c"),
                showarrow=False,
                xanchor="left"
            )
    
    # Add base label
    fig.add_annotation(
        x=3.5, y=-0.5,
        text="← BOTTOM",
        font=dict(size=12, color="#27ae60"),
        showarrow=False,
        xanchor="left"
    )
    
    fig.update_layout(
        title=f"Stack Visualization (Size: {num_items})",
        xaxis_range=[0, 5],
        yaxis_range=[-1, max(num_items + 1, 6)],
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=500,
        showlegend=False,
        plot_bgcolor="#f8f9fa"
    )
    
    return fig


if __name__ == "__main__":
    app.run(debug=True, port=8050)
