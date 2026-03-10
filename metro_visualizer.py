"""
Metro Management System - Interactive Visualizer
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import threading
import time
from datetime import datetime
from metro_system import MetroManagementSystem


# Global metro system instance
metro_system = MetroManagementSystem()

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1("🚇 Metro Management System", style={
            "textAlign": "center",
            "color": "#2c3e50",
            "marginBottom": 10,
            "fontSize": "2.5em"
        }),

        html.P("Real-time Metro Operations with Stack & Queue Data Structures",
               style={"textAlign": "center", "color": "#7f8c8d", "marginBottom": 30}),

        # Control Panel
        html.Div([
            html.Div([
                html.H3("🎛️ Control Panel", style={"color": "#2c3e50", "marginBottom": 15}),

                # Passenger Management
                html.Div([
                    html.Label("Add Passenger:", style={"fontWeight": "bold", "display": "block"}),
                    dcc.Input(id="passenger-name", type="text", placeholder="Name",
                             style={"width": "120px", "marginRight": "10px"}),
                    dcc.Dropdown(
                        id="start-station",
                        options=[{"label": s, "value": s} for s in metro_system.stations.keys()],
                        placeholder="From",
                        style={"width": "150px", "marginRight": "10px"}
                    ),
                    dcc.Dropdown(
                        id="dest-station",
                        options=[{"label": s, "value": s} for s in metro_system.stations.keys()],
                        placeholder="To",
                        style={"width": "150px", "marginRight": "10px"}
                    ),
                    dcc.Dropdown(
                        id="ticket-type",
                        options=[
                            {"label": "Regular", "value": "regular"},
                            {"label": "Student", "value": "student"},
                            {"label": "Senior", "value": "senior"}
                        ],
                        value="regular",
                        style={"width": "100px", "marginRight": "10px"}
                    ),
                    html.Button("Add Passenger", id="add-passenger-btn", n_clicks=0,
                               style={"padding": "8px 15px", "backgroundColor": "#27ae60",
                                      "color": "white", "border": "none", "borderRadius": "5px"})
                ], style={"marginBottom": "20px"}),

                # System Controls
                html.Div([
                    html.Button("▶️ Start Simulation", id="start-sim-btn", n_clicks=0,
                               style={"padding": "10px 20px", "marginRight": "10px",
                                      "backgroundColor": "#3498db", "color": "white",
                                      "border": "none", "borderRadius": "5px"}),
                    html.Button("⏸️ Stop Simulation", id="stop-sim-btn", n_clicks=0,
                               style={"padding": "10px 20px", "marginRight": "10px",
                                      "backgroundColor": "#e74c3c", "color": "white",
                                      "border": "none", "borderRadius": "5px"}),
                    html.Button("🔄 Reset System", id="reset-btn", n_clicks=0,
                               style={"padding": "10px 20px", "marginRight": "10px",
                                      "backgroundColor": "#95a5a6", "color": "white",
                                      "border": "none", "borderRadius": "5px"}),
                    html.Button("🚨 Emergency", id="emergency-btn", n_clicks=0,
                               style={"padding": "10px 20px",
                                      "backgroundColor": "#e67e22", "color": "white",
                                      "border": "none", "borderRadius": "5px"})
                ], style={"marginBottom": "20px"}),

                # Status Display
                html.Div(id="status-display", style={
                    "padding": "15px",
                    "backgroundColor": "#ecf0f1",
                    "borderRadius": "10px",
                    "marginBottom": "20px"
                }),

                # Messages
                html.Div(id="message-display", style={
                    "padding": "10px",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "fontWeight": "bold",
                    "minHeight": "30px"
                })

            ], style={
                "padding": "20px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
            })
        ], style={"maxWidth": "1200px", "margin": "0 auto"}),

        # Visualization Section
        html.Div([
            # System Overview
            html.Div([
                dcc.Graph(id="system-overview", style={"height": "400px"})
            ], style={"marginBottom": "20px"}),

            # Real-time Charts Row
            html.Div([
                html.Div([
                    dcc.Graph(id="station-status", style={"height": "300px"})
                ], style={"width": "48%", "display": "inline-block", "marginRight": "2%"}),

                html.Div([
                    dcc.Graph(id="train-status", style={"height": "300px"})
                ], style={"width": "48%", "display": "inline-block"})
            ], style={"marginBottom": "20px"}),

            # Route Visualization
            html.Div([
                dcc.Graph(id="route-visualization", style={"height": "300px"})
            ], style={"marginBottom": "20px"}),

            # Event Log
            html.Div([
                html.H4("📋 System Events", style={"color": "#2c3e50", "marginBottom": "10px"}),
                html.Div(id="event-log", style={
                    "height": "200px",
                    "overflowY": "scroll",
                    "backgroundColor": "#f8f9fa",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "border": "1px solid #dee2e6"
                })
            ], style={"marginBottom": "20px"})

        ], style={"maxWidth": "1200px", "margin": "0 auto"})

    ], style={
        "padding": "20px",
        "backgroundColor": "#f5f5f5",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif"
    }),

    # Hidden components for simulation control
    dcc.Interval(id="simulation-interval", interval=2000, n_intervals=0, disabled=True),
    dcc.Store(id="simulation-running", data=False),
    dcc.Store(id="system-data", data={})

], style={"margin": 0, "padding": 0})


# Global variables for simulation control
simulation_running = False
simulation_thread = None


def simulation_worker():
    """Background worker for simulation"""
    global simulation_running
    while simulation_running:
        try:
            metro_system.simulate_time_step()
            time.sleep(1)  # Simulate real-time delay
        except Exception as e:
            print(f"Simulation error: {e}")
            break


@callback(
    [Output("simulation-running", "data"),
     Output("simulation-interval", "disabled"),
     Output("message-display", "children"),
     Output("message-display", "style")],
    [Input("start-sim-btn", "n_clicks"),
     Input("stop-sim-btn", "n_clicks")],
    [State("simulation-running", "data")]
)
def control_simulation(start_clicks, stop_clicks, is_running):
    """Control simulation start/stop"""
    global simulation_running, simulation_thread

    ctx = dash.callback_context
    if not ctx.triggered:
        return is_running, True, "", {}

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "start-sim-btn" and not is_running:
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_worker, daemon=True)
        simulation_thread.start()

        return True, False, "▶️ Simulation Started", {
            "backgroundColor": "#d4edda", "color": "#155724", "padding": "10px",
            "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
        }

    elif button_id == "stop-sim-btn" and is_running:
        simulation_running = False
        if simulation_thread and simulation_thread.is_alive():
            simulation_thread.join(timeout=1)

        return False, True, "⏸️ Simulation Stopped", {
            "backgroundColor": "#f8d7da", "color": "#721c24", "padding": "10px",
            "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
        }

    return is_running, not is_running, "", {}


@callback(
    [Output("message-display", "children", allow_duplicate=True),
     Output("message-display", "style", allow_duplicate=True)],
    [Input("add-passenger-btn", "n_clicks"),
     Input("reset-btn", "n_clicks"),
     Input("emergency-btn", "n_clicks")],
    [State("passenger-name", "value"),
     State("start-station", "value"),
     State("dest-station", "value"),
     State("ticket-type", "value")],
    prevent_initial_call=True
)
def handle_actions(add_clicks, reset_clicks, emergency_clicks, name, start, dest, ticket_type):
    """Handle various system actions"""

    ctx = dash.callback_context
    if not ctx.triggered:
        return "", {}

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    try:
        if button_id == "add-passenger-btn":
            if not all([name, start, dest]):
                raise ValueError("Please fill all passenger fields")

            if start == dest:
                raise ValueError("Start and destination stations cannot be the same")

            passenger_id = metro_system.add_passenger(name, start, dest, ticket_type or "regular")

            return f"✓ Added passenger {name} ({passenger_id}) from {start} to {dest}", {
                "backgroundColor": "#d4edda", "color": "#155724", "padding": "10px",
                "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
            }

        elif button_id == "reset-btn":
            metro_system.reset_system()
            return "🔄 System reset completed", {
                "backgroundColor": "#d4edda", "color": "#155724", "padding": "10px",
                "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
            }

        elif button_id == "emergency-btn":
            # Emergency evacuation at a random station for demo
            stations = list(metro_system.stations.keys())
            if stations:
                station = random.choice(stations)
                evacuated = metro_system.emergency_evacuation(station)
                return f"🚨 Emergency evacuation: {evacuated} passengers evacuated from {station}", {
                    "backgroundColor": "#f8d7da", "color": "#721c24", "padding": "10px",
                    "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
                }

    except Exception as e:
        return f"✗ Error: {str(e)}", {
            "backgroundColor": "#f8d7da", "color": "#721c24", "padding": "10px",
            "borderRadius": "5px", "textAlign": "center", "fontWeight": "bold"
        }

    return "", {}


@callback(
    [Output("system-overview", "figure"),
     Output("station-status", "figure"),
     Output("train-status", "figure"),
     Output("route-visualization", "figure"),
     Output("status-display", "children"),
     Output("event-log", "children")],
    [Input("simulation-interval", "n_intervals"),
     Input("add-passenger-btn", "n_clicks"),
     Input("reset-btn", "n_clicks"),
     Input("emergency-btn", "n_clicks")]
)
def update_visualizations(n_intervals, *args):
    """Update all visualizations"""

    # Get current system status
    status = metro_system.get_system_status()

    # System Overview
    system_fig = create_system_overview(status)

    # Station Status
    station_fig = create_station_status(status)

    # Train Status
    train_fig = create_train_status(status)

    # Route Visualization
    route_fig = create_route_visualization(status)

    # Status Display
    status_display = create_status_display(status)

    # Event Log
    event_log = create_event_log(status)

    return system_fig, station_fig, train_fig, route_fig, status_display, event_log


def create_system_overview(status):
    """Create system overview visualization"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Station Utilization", "Train Load", "Active Passengers", "System Health"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "indicator"}, {"type": "indicator"}]]
    )

    # Station utilization
    stations = list(status["stations"].keys())
    utilization = [float(s["utilization"].strip('%')) for s in status["stations"].values()]

    fig.add_trace(
        go.Bar(x=stations, y=utilization, name="Station Utilization",
               marker_color='lightblue'),
        row=1, col=1
    )

    # Train load
    trains = list(status["trains"].keys())
    train_load = [float(t["utilization"].strip('%')) for t in status["trains"].values()]

    fig.add_trace(
        go.Bar(x=trains, y=train_load, name="Train Load",
               marker_color='lightgreen'),
        row=1, col=2
    )

    # Active passengers indicator
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=status["total_passengers"],
            title={"text": "Active Passengers"},
            number={"font": {"size": 40}}
        ),
        row=2, col=1
    )

    # System health indicator
    total_capacity = sum(s["capacity"] for s in status["stations"].values())
    total_waiting = sum(s["waiting"] for s in status["stations"].values())
    health_percentage = (1 - total_waiting/total_capacity) * 100 if total_capacity > 0 else 100

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=health_percentage,
            title={"text": "System Health"},
            gauge={"axis": {"range": [0, 100]},
                   "bar": {"color": "green" if health_percentage > 70 else "orange" if health_percentage > 40 else "red"}}
        ),
        row=2, col=2
    )

    fig.update_layout(height=500, showlegend=False)
    return fig


def create_station_status(status):
    """Create station status visualization"""
    stations = list(status["stations"].keys())
    waiting = [s["waiting"] for s in status["stations"].values()]
    capacity = [s["capacity"] for s in status["stations"].values()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stations,
        y=waiting,
        name="Waiting Passengers",
        marker_color='orange'
    ))

    fig.add_trace(go.Bar(
        x=stations,
        y=capacity,
        name="Capacity",
        marker_color='lightgray',
        opacity=0.3
    ))

    fig.update_layout(
        title="Station Status",
        xaxis_title="Stations",
        yaxis_title="Passengers",
        barmode='overlay',
        height=300
    )

    return fig


def create_train_status(status):
    """Create train status visualization"""
    trains = list(status["trains"].keys())
    passengers = [t["passengers"] for t in status["trains"].values()]
    capacity = [t["capacity"] for t in status["trains"].values()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=trains,
        y=passengers,
        name="Current Passengers",
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=trains,
        y=capacity,
        name="Capacity",
        marker_color='lightgray',
        opacity=0.3
    ))

    fig.update_layout(
        title="Train Status",
        xaxis_title="Trains",
        yaxis_title="Passengers",
        barmode='overlay',
        height=300
    )

    return fig


def create_route_visualization(status):
    """Create route visualization"""
    route = status["route"]

    # Create positions for stations in a line
    positions = list(range(len(route)))

    fig = go.Figure()

    # Add route line
    fig.add_trace(go.Scatter(
        x=positions,
        y=[0] * len(route),
        mode='lines+markers',
        name='Route',
        line=dict(color='blue', width=3),
        marker=dict(size=10, color='blue')
    ))

    # Add station labels
    for i, station in enumerate(route):
        fig.add_annotation(
            x=i, y=0.1,
            text=station,
            showarrow=False,
            font=dict(size=10),
            textangle=-45
        )

    # Add train positions
    for train_id, train_info in status["trains"].items():
        if train_info["location"] in route:
            pos = route.index(train_info["location"])
            fig.add_trace(go.Scatter(
                x=[pos],
                y=[0],
                mode='markers',
                name=f'Train {train_id}',
                marker=dict(size=15, symbol='diamond', color='red'),
                text=f'{train_id} ({train_info["passengers"]} passengers)'
            ))

    fig.update_layout(
        title="Metro Route & Train Positions",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        height=300,
        showlegend=True
    )

    return fig


def create_status_display(status):
    """Create status display HTML"""
    total_stations = len(status["stations"])
    total_trains = len(status["trains"])
    total_passengers = status["total_passengers"]

    total_waiting = sum(s["waiting"] for s in status["stations"].values())
    total_capacity = sum(s["capacity"] for s in status["stations"].values())

    return html.Div([
        html.Div([
            html.Span("🚉 Stations: ", style={"fontWeight": "bold"}),
            html.Span(f"{total_stations}", style={"color": "#3498db"})
        ], style={"marginRight": "30px"}),
        html.Div([
            html.Span("🚂 Trains: ", style={"fontWeight": "bold"}),
            html.Span(f"{total_trains}", style={"color": "#27ae60"})
        ], style={"marginRight": "30px"}),
        html.Div([
            html.Span("👥 Active Passengers: ", style={"fontWeight": "bold"}),
            html.Span(f"{total_passengers}", style={"color": "#9b59b6"})
        ], style={"marginRight": "30px"}),
        html.Div([
            html.Span("⏳ Waiting: ", style={"fontWeight": "bold"}),
            html.Span(f"{total_waiting}/{total_capacity}", style={"color": "#e74c3c"})
        ])
    ], style={"display": "flex", "flexWrap": "wrap"})


def create_event_log(status):
    """Create event log display"""
    events = status["system_events"]

    if not events:
        return html.P("No recent events", style={"color": "#7f8c8d", "fontStyle": "italic"})

    event_items = []
    for event in events[-10:]:  # Show last 10 events
        timestamp = datetime.now().strftime("%H:%M:%S")
        event_items.append(html.P(f"[{timestamp}] {event}",
                                style={"margin": "2px 0", "fontSize": "12px"}))

    return html.Div(event_items)


if __name__ == "__main__":
    print("🚇 Starting Metro Management System Visualizer...")
    print("Open your browser to: http://localhost:8050")
    app.run_server(debug=True, port=8050)