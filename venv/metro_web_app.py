# Metro Management System - Professional Web Application
# Modern UI inspired by Bookkaru design

import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# External stylesheets
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
]

# Database Setup
conn = sqlite3.connect('metro_web.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trains (train_id TEXT PRIMARY KEY, train_name TEXT, source TEXT, destination TEXT, departure_time TEXT, arrival_time TEXT, capacity INTEGER, available_seats INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS commuters (commuter_id TEXT PRIMARY KEY, name TEXT, email TEXT, phone TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS bookings (booking_id TEXT PRIMARY KEY, commuter_id TEXT, train_id TEXT, booking_date TEXT, status TEXT)")
conn.commit()

# App Setup
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Metro Management System"

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: #f8f9fa;
                color: #333;
            }
            
            .navbar {
                background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
                padding: 15px 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                position: sticky;
                top: 0;
                z-index: 100;
            }
            
            .navbar-brand {
                color: white;
                font-size: 24px;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .hero-section {
                background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
                color: white;
                padding: 60px 20px;
                text-align: center;
            }
            
            .hero-title {
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .hero-subtitle {
                font-size: 18px;
                font-weight: 300;
                opacity: 0.9;
                margin-bottom: 30px;
            }
            
            .search-box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.15);
                margin: -30px 20px 40px;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .search-row {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
            }
            
            .search-input {
                padding: 12px 15px !important;
                border: 2px solid #ddd !important;
                border-radius: 8px !important;
                font-size: 14px !important;
                transition: all 0.3s ease !important;
            }
            
            .search-input:focus {
                border-color: #e74c3c !important;
                box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1) !important;
            }
            
            .btn-search {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
                padding: 12px 40px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
            }
            
            .btn-search:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            .section-title {
                font-size: 32px;
                font-weight: 700;
                color: #0f3460;
                margin: 40px 0 30px;
                text-align: center;
                position: relative;
                padding-bottom: 15px;
            }
            
            .section-title:after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80px;
                height: 4px;
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                border-radius: 2px;
            }
            
            .train-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                margin-bottom: 20px;
                transition: all 0.3s ease;
                border-left: 5px solid #e74c3c;
            }
            
            .train-card:hover {
                box-shadow: 0 8px 25px rgba(0,0,0,0.12);
                transform: translateY(-2px);
            }
            
            .train-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .train-name {
                font-size: 18px;
                font-weight: 600;
                color: #0f3460;
            }
            
            .train-status {
                background: #27ae60;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }
            
            .train-route {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #ecf0f1;
            }
            
            .station {
                flex: 1;
            }
            
            .station-time {
                font-size: 18px;
                font-weight: 600;
                color: #0f3460;
            }
            
            .station-name {
                font-size: 12px;
                color: #7f8c8d;
                margin-top: 5px;
            }
            
            .train-info {
                display: flex;
                gap: 30px;
                justify-content: space-between;
                padding-top: 15px;
            }
            
            .info-item {
                text-align: center;
            }
            
            .info-value {
                font-size: 20px;
                font-weight: 600;
                color: #e74c3c;
            }
            
            .info-label {
                font-size: 12px;
                color: #7f8c8d;
                margin-top: 5px;
            }
            
            .btn-book {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
                padding: 10px 30px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 14px;
            }
            
            .btn-book:hover {
                transform: scale(1.05);
            }
            
            .tabs-section {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                padding: 30px;
                margin-bottom: 40px;
            }
            
            .tab-content {
                padding: 20px;
                background: white;
                border-radius: 10px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                text-align: center;
                border-top: 4px solid #e74c3c;
            }
            
            .stat-value {
                font-size: 32px;
                font-weight: 700;
                color: #0f3460;
                margin-bottom: 10px;
            }
            
            .stat-label {
                font-size: 14px;
                color: #7f8c8d;
                font-weight: 500;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #0f3460;
                font-size: 14px;
            }
            
            .form-input {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            
            .form-input:focus {
                border-color: #e74c3c;
                box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
                outline: none;
            }
            
            .btn-submit {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
                font-size: 16px;
            }
            
            .btn-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
            }
            
            .message {
                padding: 12px 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                font-weight: 500;
            }
            
            .message.success {
                background: #d5f4e6;
                color: #27ae60;
                border-left: 4px solid #27ae60;
            }
            
            .message.error {
                background: #fadbd8;
                color: #c0392b;
                border-left: 4px solid #c0392b;
            }
            
            .table-responsive {
                overflow-x: auto;
            }
            
            .footer {
                background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
                margin-top: 60px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout
app.layout = html.Div([
    # Navbar
    html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-subway", style={'color': '#e74c3c', 'fontSize': '28px'}),
                html.Span("Metro Management", style={'color': 'white'})
            ], className='navbar-brand')
        ], className='container')
    ], className='navbar'),
    
    # Hero Section
    html.Div([
        html.Div([
            html.H1("EXPLORE YOUR JOURNEY", className='hero-title'),
            html.P("Fast, Reliable, and Convenient Metro Services", className='hero-subtitle'),
        ], className='container')
    ], className='hero-section'),
    
    # Search Box
    html.Div([
        html.Div([
            html.Div([
                dcc.Input(
                    id='search-from',
                    placeholder='From Station',
                    type='text',
                    className='search-input',
                    style={'flex': '1', 'minWidth': '150px'}
                ),
                dcc.Input(
                    id='search-to',
                    placeholder='To Station',
                    type='text',
                    className='search-input',
                    style={'flex': '1', 'minWidth': '150px'}
                ),
                dcc.Input(
                    id='search-date',
                    placeholder='YYYY-MM-DD',
                    type='text',
                    className='search-input',
                    style={'flex': '1', 'minWidth': '150px'}
                ),
                html.Button('SEARCH', id='search-btn', className='btn-search')
            ], className='search-row')
        ], className='search-box')
    ], className='hero-section', style={'paddingTop': '0', 'paddingBottom': '0'}),
    
    # Main Content
    html.Div([
        # Dashboard Stats
        html.Div([
            html.H2("Dashboard Overview", className='section-title'),
            html.Div(id='stats-container', className='stats-grid')
        ], className='container', style={'marginBottom': '40px'}),
        
        # Tabs Section
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='🚇 Available Trains', children=[
                    html.Div(id='trains-list', className='tab-content')
                ], className='tabs-section'),
                
                dcc.Tab(label='👥 Add Commuter', children=[
                    html.Div([
                        html.Div([
                            html.H3("Register New Commuter", style={'marginBottom': '20px', 'color': '#0f3460'}),
                            html.Div([
                                html.Div([
                                    html.Label("Commuter ID", className='form-label'),
                                    dcc.Input(id='commuter-id', type='text', placeholder='Enter ID', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Full Name", className='form-label'),
                                    dcc.Input(id='commuter-name', type='text', placeholder='Enter Name', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Email", className='form-label'),
                                    dcc.Input(id='commuter-email', type='email', placeholder='Enter Email', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Phone", className='form-label'),
                                    dcc.Input(id='commuter-phone', type='tel', placeholder='Enter Phone', className='form-input')
                                ], style={'marginBottom': '20px'}),
                                html.Button('Register Commuter', id='add-commuter-btn', className='btn-submit'),
                                html.Div(id='commuter-msg', className='message', style={'display': 'none'})
                            ])
                        ], style={'maxWidth': '500px', 'margin': '0 auto'})
                    ], className='tab-content')
                ]),
                
                dcc.Tab(label='🎫 Add Train', children=[
                    html.Div([
                        html.Div([
                            html.H3("Add New Train", style={'marginBottom': '20px', 'color': '#0f3460'}),
                            html.Div([
                                html.Div([
                                    html.Label("Train ID", className='form-label'),
                                    dcc.Input(id='train-id', type='text', placeholder='Enter Train ID', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Train Name", className='form-label'),
                                    dcc.Input(id='train-name', type='text', placeholder='Enter Train Name', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("From Station", className='form-label'),
                                    dcc.Input(id='train-from', type='text', placeholder='Enter Source', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("To Station", className='form-label'),
                                    dcc.Input(id='train-to', type='text', placeholder='Enter Destination', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Departure Time", className='form-label'),
                                    dcc.Input(id='train-dept', type='text', placeholder='HH:MM (e.g., 08:30)', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Arrival Time", className='form-label'),
                                    dcc.Input(id='train-arr', type='text', placeholder='HH:MM (e.g., 10:45)', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Total Capacity", className='form-label'),
                                    dcc.Input(id='train-capacity', type='number', placeholder='Enter Capacity', className='form-input')
                                ], style={'marginBottom': '20px'}),
                                html.Button('Add Train', id='add-train-btn', className='btn-submit'),
                                html.Div(id='train-msg', className='message', style={'display': 'none'})
                            ])
                        ], style={'maxWidth': '500px', 'margin': '0 auto'})
                    ], className='tab-content')
                ]),
                
                dcc.Tab(label='🎫 Book Ticket', children=[
                    html.Div([
                        html.Div([
                            html.H3("Book Your Ticket", style={'marginBottom': '20px', 'color': '#0f3460'}),
                            html.Div([
                                html.Div([
                                    html.Label("Booking ID", className='form-label'),
                                    dcc.Input(id='booking-id', type='text', placeholder='Enter Booking ID', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Commuter ID", className='form-label'),
                                    dcc.Input(id='booking-commuter-id', type='text', placeholder='Enter Commuter ID', className='form-input')
                                ], style={'marginBottom': '15px'}),
                                html.Div([
                                    html.Label("Train ID", className='form-label'),
                                    dcc.Input(id='booking-train-id', type='text', placeholder='Enter Train ID', className='form-input')
                                ], style={'marginBottom': '20px'}),
                                html.Button('Book Ticket', id='add-booking-btn', className='btn-submit'),
                                html.Div(id='booking-msg', className='message', style={'display': 'none'})
                            ])
                        ], style={'maxWidth': '500px', 'margin': '0 auto'})
                    ], className='tab-content')
                ])
            ], style={'borderRadius': '12px'})
        ], className='container', style={'marginBottom': '40px'})
        
    ], style={'paddingTop': '0'}),
    
    # Footer
    html.Div([
        html.Div([
            html.H4("Metro Management System", style={'marginBottom': '10px'}),
            html.P("© 2026 All rights reserved. Fast and efficient urban transit solution.")
        ], className='container')
    ], className='footer')
])

# Callbacks
@callback(
    Output('stats-container', 'children'),
    Input('search-btn', 'n_clicks')
)
def update_stats(n):
    cursor.execute("SELECT COUNT(*) FROM trains")
    trains_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM commuters")
    commuters_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM bookings")
    bookings_count = cursor.fetchone()[0]
    
    return [
        html.Div([
            html.Div(trains_count, className='stat-value'),
            html.Div("Active Trains", className='stat-label')
        ], className='stat-card'),
        html.Div([
            html.Div(commuters_count, className='stat-value'),
            html.Div("Registered Commuters", className='stat-label')
        ], className='stat-card'),
        html.Div([
            html.Div(bookings_count, className='stat-value'),
            html.Div("Total Bookings", className='stat-label')
        ], className='stat-card'),
    ]

@callback(
    Output('trains-list', 'children'),
    Input('search-btn', 'n_clicks')
)
def update_trains(n):
    try:
        df = pd.read_sql('SELECT * FROM trains', conn)
        if df.empty:
            return html.Div("No trains available. Add some trains to get started!", 
                          style={'textAlign': 'center', 'padding': '40px', 'color': '#7f8c8d'})
        
        trains = []
        for _, row in df.iterrows():
            train_card = html.Div([
                html.Div([
                    html.Div(row['train_name'], className='train-name'),
                    html.Div('Available', className='train-status')
                ], className='train-header'),
                
                html.Div([
                    html.Div([
                        html.Div(row['departure_time'] or 'N/A', className='station-time'),
                        html.Div(row['source'], className='station-name')
                    ], className='station'),
                    html.Div('➜', style={'fontSize': '24px', 'color': '#bdc3c7', 'alignSelf': 'center'}),
                    html.Div([
                        html.Div(row['arrival_time'] or 'N/A', className='station-time'),
                        html.Div(row['destination'], className='station-name')
                    ], className='station')
                ], className='train-route'),
                
                html.Div([
                    html.Div([
                        html.Div(f"{row['available_seats']}/{row['capacity']}", className='info-value'),
                        html.Div('Seats Available', className='info-label')
                    ], className='info-item'),
                    html.Button('BOOK NOW', className='btn-book')
                ], className='train-info')
            ], className='train-card')
            trains.append(train_card)
        
        return html.Div(trains)
    except:
        return html.Div("Error loading trains", style={'color': '#c0392b'})

@callback(
    Output('commuter-msg', 'children'),
    Output('commuter-msg', 'style'),
    Input('add-commuter-btn', 'n_clicks'),
    State('commuter-id', 'value'),
    State('commuter-name', 'value'),
    State('commuter-email', 'value'),
    State('commuter-phone', 'value'),
    prevent_initial_call=True
)
def add_commuter(n, cid, name, email, phone):
    if n and cid and name and email and phone:
        try:
            cursor.execute("INSERT INTO commuters VALUES (?,?,?,?)", (cid, name, email, phone))
            conn.commit()
            return "✅ Commuter registered successfully!", {'display': 'block'}
        except:
            return "❌ Commuter ID already exists!", {'display': 'block'}
    return "", {'display': 'none'}

@callback(
    Output('train-msg', 'children'),
    Output('train-msg', 'style'),
    Input('add-train-btn', 'n_clicks'),
    State('train-id', 'value'),
    State('train-name', 'value'),
    State('train-from', 'value'),
    State('train-to', 'value'),
    State('train-dept', 'value'),
    State('train-arr', 'value'),
    State('train-capacity', 'value'),
    prevent_initial_call=True
)
def add_train(n, tid, name, source, dest, dept, arr, capacity):
    if n and tid and name and source and dest and capacity:
        try:
            cursor.execute("INSERT INTO trains VALUES (?,?,?,?,?,?,?,?)", 
                         (tid, name, source, dest, dept or '', arr or '', int(capacity), int(capacity)))
            conn.commit()
            return "✅ Train added successfully!", {'display': 'block'}
        except:
            return "❌ Train ID already exists!", {'display': 'block'}
    return "", {'display': 'none'}

@callback(
    Output('booking-msg', 'children'),
    Output('booking-msg', 'style'),
    Input('add-booking-btn', 'n_clicks'),
    State('booking-id', 'value'),
    State('booking-commuter-id', 'value'),
    State('booking-train-id', 'value'),
    prevent_initial_call=True
)
def add_booking(n, bid, cid, tid):
    if n and bid and cid and tid:
        try:
            cursor.execute("INSERT INTO bookings VALUES (?,?,?,?,?)", 
                         (bid, cid, tid, datetime.now().strftime('%Y-%m-%d'), 'Confirmed'))
            conn.commit()
            return "✅ Ticket booked successfully!", {'display': 'block'}
        except:
            return "❌ Booking ID already exists!", {'display': 'block'}
    return "", {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=True, port=8050)
