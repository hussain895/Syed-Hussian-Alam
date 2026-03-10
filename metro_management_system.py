# Professional Metro Management System - MetroHub
# Complete metro ticket reservation and management platform

import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# External stylesheets
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
]

# Database Setup
conn = sqlite3.connect('metro_management.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS metro_routes (
    route_id TEXT PRIMARY KEY,
    metro_line TEXT,
    route_number TEXT,
    departure_station TEXT,
    arrival_station TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    duration TEXT,
    fare REAL,
    seats_available INTEGER,
    seats_total INTEGER,
    train_type TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ticket_bookings (
    ticket_id TEXT PRIMARY KEY,
    passenger_name TEXT,
    email TEXT,
    phone TEXT,
    route_id TEXT,
    passengers INTEGER,
    booking_date TEXT,
    status TEXT
)''')

conn.commit()

# App Setup
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "MetroHub - Metro Ticket Booking System"

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

            html, body {
                font-family: 'Poppins', sans-serif;
                background: #f5f7fa;
                color: #333;
            }

            /* Navbar */
            .navbar {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                padding: 15px 0;
                box-shadow: 0 4px 20px rgba(44, 62, 80, 0.2);
                position: sticky;
                top: 0;
                z-index: 1000;
            }

            .navbar-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .navbar-brand {
                display: flex;
                align-items: center;
                gap: 10px;
                color: white;
                font-size: 24px;
                font-weight: 700;
                text-decoration: none;
            }

            .navbar-brand i {
                color: #3498db;
                font-size: 28px;
            }

            .navbar-menu {
                display: flex;
                gap: 30px;
                align-items: center;
            }

            .navbar-menu a {
                color: white;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.3s ease;
            }

            .navbar-menu a:hover {
                color: #3498db;
            }

            .login-btn {
                background: #3498db;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .login-btn:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }

            /* Hero Section */
            .hero {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 60px 20px;
                text-align: center;
            }

            .hero-content {
                max-width: 1400px;
                margin: 0 auto;
            }

            .hero h1 {
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            }

            .hero p {
                font-size: 18px;
                opacity: 0.95;
                margin-bottom: 30px;
            }

            /* Search Box */
            .search-container {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                margin: -30px 20px 40px;
                max-width: 1400px;
                margin-left: auto;
                margin-right: auto;
            }

            .search-tabs {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
                border-bottom: 2px solid #e8eef5;
                padding-bottom: 15px;
            }

            .search-tab {
                background: none;
                border: none;
                padding: 10px 0;
                cursor: pointer;
                font-weight: 600;
                color: #7f8c8d;
                transition: all 0.3s ease;
                position: relative;
            }

            .search-tab.active {
                color: #2c3e50;
            }

            .search-tab.active::after {
                content: '';
                position: absolute;
                bottom: -17px;
                left: 0;
                width: 100%;
                height: 3px;
                background: #3498db;
                border-radius: 2px;
            }

            .search-form {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                align-items: end;
            }

            .form-group {
                display: flex;
                flex-direction: column;
            }

            .form-label {
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 8px;
                font-size: 13px;
            }

            .form-input {
                padding: 12px 15px;
                border: 2px solid #e8eef5;
                border-radius: 8px;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
                transition: all 0.3s ease;
            }

            .form-input:focus {
                outline: none;
                border-color: #3498db;
                box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
            }

            .search-btn {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                padding: 12px 40px;
                border: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
            }

            .search-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(52, 152, 219, 0.4);
            }

            /* Main Content */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
            }

            .section-title {
                font-size: 32px;
                font-weight: 700;
                color: #2c3e50;
                margin: 50px 0 30px;
                text-align: center;
                position: relative;
                padding-bottom: 15px;
            }

            .section-title::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80px;
                height: 3px;
                background: #3498db;
                border-radius: 2px;
            }

            /* Route Cards */
            .routes-container {
                display: grid;
                gap: 20px;
                margin-bottom: 40px;
            }

            .route-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
                border-left: 5px solid #3498db;
            }

            .route-card:hover {
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
                transform: translateY(-3px);
            }

            .route-header {
                display: flex;
                justify-content: space-between;
                align-items: start;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #e8eef5;
            }

            .metro-info {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .metro-logo {
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 18px;
            }

            .metro-details h3 {
                font-size: 16px;
                color: #2c3e50;
                margin-bottom: 3px;
            }

            .metro-details p {
                font-size: 12px;
                color: #7f8c8d;
            }

            .fare-tag {
                text-align: right;
            }

            .fare {
                font-size: 28px;
                font-weight: 700;
                color: #3498db;
            }

            .fare-label {
                font-size: 12px;
                color: #7f8c8d;
            }

            .route-path {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                gap: 20px;
            }

            .route-station {
                flex: 1;
                text-align: center;
            }

            .route-time {
                font-size: 22px;
                font-weight: 700;
                color: #2c3e50;
            }

            .route-station-name {
                font-size: 12px;
                color: #7f8c8d;
                margin-top: 5px;
            }

            .route-arrow {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                color: #bdc3c7;
                flex: 0.5;
            }

            .route-arrow i {
                font-size: 24px;
            }

            .route-duration {
                font-size: 11px;
                color: #7f8c8d;
                background: #f5f7fa;
                padding: 4px 8px;
                border-radius: 4px;
            }

            .route-info {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 0;
                border-top: 1px solid #e8eef5;
            }

            .info-item {
                text-align: center;
                flex: 1;
            }

            .info-value {
                font-size: 18px;
                font-weight: 700;
                color: #2c3e50;
            }

            .info-label {
                font-size: 11px;
                color: #7f8c8d;
                margin-top: 3px;
            }

            .route-actions {
                display: flex;
                gap: 10px;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #e8eef5;
            }

            .btn-select {
                flex: 1;
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                color: white;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .btn-select:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3);
            }

            /* Stats */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }

            .stat-card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                text-align: center;
                border-top: 4px solid #3498db;
            }

            .stat-value {
                font-size: 36px;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 10px;
            }

            .stat-label {
                font-size: 14px;
                color: #7f8c8d;
            }

            /* Tabs */
            .tabs-container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                padding: 30px;
                margin-bottom: 40px;
            }

            .tab-content {
                padding: 20px;
            }

            .form-section {
                max-width: 600px;
                margin: 0 auto;
            }

            .form-section h3 {
                color: #2c3e50;
                margin-bottom: 20px;
                font-size: 20px;
            }

            .form-section .form-group {
                margin-bottom: 15px;
            }

            .message {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                font-weight: 600;
                display: none;
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

            .message.show {
                display: block;
            }

            /* Footer */
            .footer {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 40px 20px;
                margin-top: 60px;
                text-align: center;
            }

            .footer-content {
                max-width: 1400px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 30px;
                text-align: left;
                margin-bottom: 30px;
            }

            .footer-section h4 {
                margin-bottom: 15px;
            }

            .footer-section ul {
                list-style: none;
            }

            .footer-section ul li {
                margin-bottom: 10px;
            }

            .footer-section ul li a {
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                transition: color 0.3s ease;
            }

            .footer-section ul li a:hover {
                color: #3498db;
            }

            .footer-bottom {
                text-align: center;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                padding-top: 20px;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .hero h1 {
                    font-size: 32px;
                }

                .search-form {
                    grid-template-columns: 1fr;
                }

                .route-path {
                    flex-direction: column;
                    gap: 15px;
                }

                .navbar-menu {
                    gap: 15px;
                    font-size: 14px;
                }
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
                html.I(className="fas fa-subway", style={'color': '#3498db', 'fontSize': '28px'}),
                html.Span("MetroHub")
            ], className='navbar-brand'),
            html.Div([
                html.A("Home", href="#", style={'color': 'white'}),
                html.A("Routes", href="#", style={'color': 'white'}),
                html.A("About", href="#", style={'color': 'white'}),
                html.Button("Login", className='login-btn')
            ], className='navbar-menu')
        ], className='navbar-container')
    ], className='navbar'),

    # Hero Section
    html.Div([
        html.Div([
            html.H1("TRAVEL WITH US"),
            html.H1("EXPLORE THE CITY", style={'color': '#3498db'}),
            html.P("Find and book metro tickets at the lowest and most affordable fares")
        ], className='hero-content')
    ], className='hero'),

    # Search Box
    html.Div([
        html.Div([
            html.Div([
                html.Button("Round Trip", id="tab-round", className='search-tab active'),
                html.Button("One Way", id="tab-oneway", className='search-tab'),
                html.Button("Multi-Stop", id="tab-multi", className='search-tab'),
            ], className='search-tabs'),

            html.Div([
                html.Div([
                    html.Label("Departure Station", className='form-label'),
                    dcc.Input(id='from-station', type='text', placeholder='From', className='form-input')
                ], className='form-group'),

                html.Div([
                    html.Label("Arrival Station", className='form-label'),
                    dcc.Input(id='to-station', type='text', placeholder='To', className='form-input')
                ], className='form-group'),

                html.Div([
                    html.Label("Departure Date", className='form-label'),
                    dcc.Input(id='depart-date', type='text', placeholder='YYYY-MM-DD', className='form-input')
                ], className='form-group'),

                html.Div([
                    html.Label("Return Date", className='form-label'),
                    dcc.Input(id='return-date', type='text', placeholder='YYYY-MM-DD', className='form-input')
                ], className='form-group'),

                html.Div([
                    html.Label("Passengers", className='form-label'),
                    dcc.Input(id='passengers', type='number', placeholder='1', value='1', className='form-input', min=1)
                ], className='form-group'),

                html.Button("SEARCH ROUTES", id='search-routes-btn', className='search-btn')
            ], className='search-form')
        ], className='search-container')
    ], className='hero', style={'paddingTop': '0', 'paddingBottom': '0'}),

    # Main Content
    html.Div([
        # Stats
        html.H2("Book Your Metro Ticket in Just 3 Steps", className='section-title', style={'marginTop': '40px'}),
        html.Div([
            html.Div([
                html.Div([html.I(className="fas fa-search", style={'fontSize': '32px', 'color': '#3498db'})], className='metro-logo'),
                html.Div([
                    html.H3("Search"),
                    html.P("Find your perfect route")
                ], className='metro-details')
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-check-circle", style={'fontSize': '32px', 'color': '#3498db'})], className='metro-logo'),
                html.Div([
                    html.H3("Select"),
                    html.P("Choose your preferred route")
                ], className='metro-details')
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-credit-card", style={'fontSize': '32px', 'color': '#3498db'})], className='metro-logo'),
                html.Div([
                    html.H3("Book"),
                    html.P("Complete your booking")
                ], className='metro-details')
            ], className='stat-card'),
        ], className='stats-grid'),

        # Routes List
        html.H2("Available Metro Routes", className='section-title'),
        html.Div(id='routes-list', className='routes-container'),

        # Book Ticket Tab
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='🚇 Book a Ticket', children=[
                    html.Div([
                        html.Div([
                            html.H3("Complete Your Booking"),
                            html.Div([
                                html.Div([
                                    html.Label("Full Name", className='form-label'),
                                    dcc.Input(id='book-name', type='text', placeholder='Enter your name', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Email", className='form-label'),
                                    dcc.Input(id='book-email', type='email', placeholder='Enter your email', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Phone", className='form-label'),
                                    dcc.Input(id='book-phone', type='tel', placeholder='Enter your phone', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Route ID", className='form-label'),
                                    dcc.Input(id='book-route-id', type='text', placeholder='Select a route', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Number of Passengers", className='form-label'),
                                    dcc.Input(id='book-passengers', type='number', value='1', className='form-input', min=1)
                                ], className='form-group'),
                                html.Div(id='booking-msg', className='message'),
                                html.Button('COMPLETE BOOKING', id='complete-booking-btn', className='btn-select',
                                          style={'background': 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)', 'marginTop': '10px'})
                            ], className='form-section')
                        ], className='tab-content')
                    ])
                ]),

                dcc.Tab(label='➕ Add New Route', children=[
                    html.Div([
                        html.Div([
                            html.H3("Add New Metro Route to System"),
                            html.Div([
                                html.Div([
                                    html.Label("Route ID", className='form-label'),
                                    dcc.Input(id='add-route-id', type='text', placeholder='RT001', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Metro Line", className='form-label'),
                                    dcc.Input(id='add-metro-line', type='text', placeholder='Red Line', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Route Number", className='form-label'),
                                    dcc.Input(id='add-route-number', type='text', placeholder='R001', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("From Station", className='form-label'),
                                    dcc.Input(id='add-from-station', type='text', placeholder='Central Station', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("To Station", className='form-label'),
                                    dcc.Input(id='add-to-station', type='text', placeholder='Airport Station', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Departure Time", className='form-label'),
                                    dcc.Input(id='add-dept-time', type='text', placeholder='08:30', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Arrival Time", className='form-label'),
                                    dcc.Input(id='add-arr-time', type='text', placeholder='09:15', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Duration", className='form-label'),
                                    dcc.Input(id='add-duration', type='text', placeholder='45 mins', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Fare (PKR)", className='form-label'),
                                    dcc.Input(id='add-fare', type='number', placeholder='150', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Available Seats", className='form-label'),
                                    dcc.Input(id='add-seats', type='number', placeholder='200', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Train Type", className='form-label'),
                                    dcc.Input(id='add-train-type', type='text', placeholder='Express Train', className='form-input')
                                ], className='form-group'),
                                html.Div(id='add-route-msg', className='message'),
                                html.Button('ADD ROUTE', id='add-route-btn', className='btn-select',
                                          style={'background': 'linear-gradient(135deg, #27ae60 0%, #229954 100%)', 'marginTop': '10px'})
                            ], className='form-section')
                        ], className='tab-content')
                    ])
                ])
            ], style={'borderRadius': '12px'})
        ], className='tabs-container', style={'marginBottom': '40px'})

    ], className='container'),

    # Footer
    html.Div([
        html.Div([
            html.Div([
                html.H4("About MetroHub"),
                html.Ul([
                    html.Li(html.A("About Us", href="#")),
                    html.Li(html.A("Contact Us", href="#")),
                    html.Li(html.A("Blog", href="#"))
                ])
            ], className='footer-section'),
            html.Div([
                html.H4("Quick Links"),
                html.Ul([
                    html.Li(html.A("Search Routes", href="#")),
                    html.Li(html.A("My Tickets", href="#")),
                    html.Li(html.A("Help & Support", href="#"))
                ])
            ], className='footer-section'),
            html.Div([
                html.H4("Policies"),
                html.Ul([
                    html.Li(html.A("Privacy Policy", href="#")),
                    html.Li(html.A("Terms & Conditions", href="#")),
                    html.Li(html.A("Cancellation Policy", href="#"))
                ])
            ], className='footer-section'),
        ], className='footer-content'),
        html.Div("© 2026 MetroHub. All rights reserved. Your trusted partner in metro travel.", className='footer-bottom')
    ], className='footer')
])

# Callbacks
@callback(
    Output('routes-list', 'children'),
    Input('search-routes-btn', 'n_clicks'),
    State('from-station', 'value'),
    State('to-station', 'value'),
    prevent_initial_call=False
)
def display_routes(n, from_station, to_station):
    try:
        df = pd.read_sql('SELECT * FROM metro_routes', conn)
        if df.empty:
            return html.Div([
                html.Div([
                    html.I(className="fas fa-subway", style={'fontSize': '48px', 'color': '#bdc3c7', 'marginBottom': '10px'}),
                    html.P("No routes available. Add routes to get started!", style={'color': '#7f8c8d', 'fontSize': '16px'})
                ], style={'textAlign': 'center', 'padding': '40px'})
            ])

        routes = []
        for _, row in df.iterrows():
            route = html.Div([
                html.Div([
                    html.Div([
                        html.Div(row['metro_line'][:2].upper(), className='metro-logo'),
                        html.Div([
                            html.H3(f"{row['metro_line']} - {row['route_number']}"),
                            html.P(f"{row['train_type']}")
                        ], className='metro-details')
                    ], className='metro-info'),
                    html.Div([
                        html.Div("PKR ", style={'fontSize': '14px', 'color': '#7f8c8d'}),
                        html.Div(f"{row['fare']:,.0f}", className='fare')
                    ], className='fare-tag')
                ], className='route-header'),

                html.Div([
                    html.Div([
                        html.Div(row['departure_time'], className='route-time'),
                        html.Div(row['departure_station'], className='route-station-name')
                    ], className='route-station'),
                    html.Div([
                        html.I(className="fas fa-arrow-right"),
                        html.Div(row['duration'], className='route-duration')
                    ], className='route-arrow'),
                    html.Div([
                        html.Div(row['arrival_time'], className='route-time'),
                        html.Div(row['arrival_station'], className='route-station-name')
                    ], className='route-station')
                ], className='route-path'),

                html.Div([
                    html.Div([
                        html.Div(f"{row['seats_available']}/{row['seats_total']}", className='info-value'),
                        html.Div('Seats Available', className='info-label')
                    ], className='info-item'),
                    html.Div([
                        html.Div("Direct", className='info-value'),
                        html.Div('Route Type', className='info-label')
                    ], className='info-item'),
                ], className='route-info'),

                html.Div([
                    html.Button('SELECT & BOOK', id={'type': 'select-route', 'index': row['route_id']},
                              className='btn-select')
                ], className='route-actions')
            ], className='route-card')
            routes.append(route)

        return html.Div(routes)
    except:
        return html.Div("Error loading routes", style={'color': '#c0392b', 'textAlign': 'center', 'padding': '40px'})

@callback(
    Output('add-route-msg', 'children'),
    Output('add-route-msg', 'className'),
    Input('add-route-btn', 'n_clicks'),
    State('add-route-id', 'value'),
    State('add-metro-line', 'value'),
    State('add-route-number', 'value'),
    State('add-from-station', 'value'),
    State('add-to-station', 'value'),
    State('add-dept-time', 'value'),
    State('add-arr-time', 'value'),
    State('add-duration', 'value'),
    State('add-fare', 'value'),
    State('add-seats', 'value'),
    State('add-train-type', 'value'),
    prevent_initial_call=True
)
def add_route(n, rid, metro_line, rnumber, from_s, to_s, dept, arr, dur, fare, seats, train_type):
    if all([rid, metro_line, rnumber, from_s, to_s, dept, arr, dur, fare, seats, train_type]):
        try:
            cursor.execute('''INSERT INTO metro_routes VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                         (rid, metro_line, rnumber, from_s, to_s, dept, arr, dur, float(fare), int(seats), int(seats), train_type))
            conn.commit()
            return "✅ Route added successfully!", "message success show"
        except:
            return "❌ Route ID already exists!", "message error show"
    return "❌ Please fill all fields", "message error show"

@callback(
    Output('booking-msg', 'children'),
    Output('booking-msg', 'className'),
    Input('complete-booking-btn', 'n_clicks'),
    State('book-name', 'value'),
    State('book-email', 'value'),
    State('book-phone', 'value'),
    State('book-route-id', 'value'),
    State('book-passengers', 'value'),
    prevent_initial_call=True
)
def complete_booking(n, name, email, phone, rid, passengers):
    if all([name, email, phone, rid, passengers]):
        try:
            tid = f"TK{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute('''INSERT INTO ticket_bookings VALUES (?,?,?,?,?,?,?,?)''',
                         (tid, name, email, phone, rid, int(passengers),
                          datetime.now().strftime('%Y-%m-%d'), 'Confirmed'))
            conn.commit()
            return f"✅ Ticket booked successfully! Ticket ID: {tid}", "message success show"
        except:
            return "❌ Booking failed. Please try again.", "message error show"
    return "❌ Please fill all fields", "message error show"

if __name__ == '__main__':
    app.run(debug=True, port=8050)