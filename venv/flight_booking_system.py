# Professional Flight Booking System - Bookkaru Style
# Complete airline ticket reservation platform

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
conn = sqlite3.connect('flight_booking.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
    flight_id TEXT PRIMARY KEY,
    airline TEXT,
    flight_number TEXT,
    departure_city TEXT,
    arrival_city TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    duration TEXT,
    price REAL,
    seats_available INTEGER,
    seats_total INTEGER,
    aircraft_type TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    passenger_name TEXT,
    email TEXT,
    phone TEXT,
    flight_id TEXT,
    passengers INTEGER,
    booking_date TEXT,
    status TEXT
)''')

conn.commit()

# App Setup
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "FlightHub - Book Flights Online"

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
                background: linear-gradient(135deg, #003f7f 0%, #0055b8 100%);
                padding: 15px 0;
                box-shadow: 0 4px 20px rgba(0, 63, 127, 0.2);
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
                color: #ff6b35;
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
                color: #ff6b35;
            }
            
            .login-btn {
                background: #ff6b35;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .login-btn:hover {
                background: #ff5722;
                transform: translateY(-2px);
            }
            
            /* Hero Section */
            .hero {
                background: linear-gradient(135deg, #003f7f 0%, #0055b8 100%);
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
                color: #003f7f;
            }
            
            .search-tab.active::after {
                content: '';
                position: absolute;
                bottom: -17px;
                left: 0;
                width: 100%;
                height: 3px;
                background: #ff6b35;
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
                color: #003f7f;
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
                border-color: #ff6b35;
                box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
            }
            
            .search-btn {
                background: linear-gradient(135deg, #ff6b35 0%, #ff5722 100%);
                color: white;
                padding: 12px 40px;
                border: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
            }
            
            .search-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 25px rgba(255, 107, 53, 0.4);
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
                color: #003f7f;
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
                background: #ff6b35;
                border-radius: 2px;
            }
            
            /* Flight Cards */
            .flights-container {
                display: grid;
                gap: 20px;
                margin-bottom: 40px;
            }
            
            .flight-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
                border-left: 5px solid #ff6b35;
            }
            
            .flight-card:hover {
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
                transform: translateY(-3px);
            }
            
            .flight-header {
                display: flex;
                justify-content: space-between;
                align-items: start;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #e8eef5;
            }
            
            .airline-info {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .airline-logo {
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #003f7f 0%, #0055b8 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 18px;
            }
            
            .airline-details h3 {
                font-size: 16px;
                color: #003f7f;
                margin-bottom: 3px;
            }
            
            .airline-details p {
                font-size: 12px;
                color: #7f8c8d;
            }
            
            .price-tag {
                text-align: right;
            }
            
            .price {
                font-size: 28px;
                font-weight: 700;
                color: #ff6b35;
            }
            
            .price-label {
                font-size: 12px;
                color: #7f8c8d;
            }
            
            .flight-route {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                gap: 20px;
            }
            
            .flight-city {
                flex: 1;
                text-align: center;
            }
            
            .flight-time {
                font-size: 22px;
                font-weight: 700;
                color: #003f7f;
            }
            
            .flight-city-name {
                font-size: 12px;
                color: #7f8c8d;
                margin-top: 5px;
            }
            
            .flight-arrow {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                color: #bdc3c7;
                flex: 0.5;
            }
            
            .flight-arrow i {
                font-size: 24px;
            }
            
            .flight-duration {
                font-size: 11px;
                color: #7f8c8d;
                background: #f5f7fa;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            .flight-info {
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
                color: #003f7f;
            }
            
            .info-label {
                font-size: 11px;
                color: #7f8c8d;
                margin-top: 3px;
            }
            
            .flight-actions {
                display: flex;
                gap: 10px;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #e8eef5;
            }
            
            .btn-select {
                flex: 1;
                background: linear-gradient(135deg, #ff6b35 0%, #ff5722 100%);
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
                box-shadow: 0 6px 20px rgba(255, 107, 53, 0.3);
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
                border-top: 4px solid #ff6b35;
            }
            
            .stat-value {
                font-size: 36px;
                font-weight: 700;
                color: #003f7f;
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
                color: #003f7f;
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
                background: linear-gradient(135deg, #003f7f 0%, #0055b8 100%);
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
                color: #ff6b35;
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
                
                .flight-route {
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
                html.I(className="fas fa-plane", style={'color': '#ff6b35', 'fontSize': '28px'}),
                html.Span("FlightHub")
            ], className='navbar-brand'),
            html.Div([
                html.A("Home", href="#", style={'color': 'white'}),
                html.A("Flights", href="#", style={'color': 'white'}),
                html.A("About", href="#", style={'color': 'white'}),
                html.Button("Login", className='login-btn')
            ], className='navbar-menu')
        ], className='navbar-container')
    ], className='navbar'),
    
    # Hero Section
    html.Div([
        html.Div([
            html.H1("TRAVEL WITH US"),
            html.H1("EXPLORE THE WORLD", style={'color': '#ff6b35'}),
            html.P("Find and book flights at the lowest and most affordable prices")
        ], className='hero-content')
    ], className='hero'),
    
    # Search Box
    html.Div([
        html.Div([
            html.Div([
                html.Button("Round Trip", id="tab-round", className='search-tab active'),
                html.Button("One Way", id="tab-oneway", className='search-tab'),
                html.Button("Multi-City", id="tab-multi", className='search-tab'),
            ], className='search-tabs'),
            
            html.Div([
                html.Div([
                    html.Label("Departure City", className='form-label'),
                    dcc.Input(id='from-city', type='text', placeholder='From', className='form-input')
                ], className='form-group'),
                
                html.Div([
                    html.Label("Arrival City", className='form-label'),
                    dcc.Input(id='to-city', type='text', placeholder='To', className='form-input')
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
                
                html.Button("SEARCH FLIGHTS", id='search-flights-btn', className='search-btn')
            ], className='search-form')
        ], className='search-container')
    ], className='hero', style={'paddingTop': '0', 'paddingBottom': '0'}),
    
    # Main Content
    html.Div([
        # Stats
        html.H2("Book Your Flight in Just 3 Steps", className='section-title', style={'marginTop': '40px'}),
        html.Div([
            html.Div([
                html.Div([html.I(className="fas fa-search", style={'fontSize': '32px', 'color': '#ff6b35'})], className='airline-logo'),
                html.Div([
                    html.H3("Search"),
                    html.P("Find your perfect flight")
                ], className='airline-details')
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-check-circle", style={'fontSize': '32px', 'color': '#ff6b35'})], className='airline-logo'),
                html.Div([
                    html.H3("Select"),
                    html.P("Choose your preferred flight")
                ], className='airline-details')
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-credit-card", style={'fontSize': '32px', 'color': '#ff6b35'})], className='airline-logo'),
                html.Div([
                    html.H3("Book"),
                    html.P("Complete your booking")
                ], className='airline-details')
            ], className='stat-card'),
        ], className='stats-grid'),
        
        # Flights List
        html.H2("Available Flights", className='section-title'),
        html.Div(id='flights-list', className='flights-container'),
        
        # Book Flight Tab
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='✈️ Book a Flight', children=[
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
                                    html.Label("Flight ID", className='form-label'),
                                    dcc.Input(id='book-flight-id', type='text', placeholder='Select a flight', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Number of Passengers", className='form-label'),
                                    dcc.Input(id='book-passengers', type='number', value='1', className='form-input', min=1)
                                ], className='form-group'),
                                html.Div(id='booking-msg', className='message'),
                                html.Button('COMPLETE BOOKING', id='complete-booking-btn', className='btn-select', 
                                          style={'background': 'linear-gradient(135deg, #ff6b35 0%, #ff5722 100%)', 'marginTop': '10px'})
                            ], className='form-section')
                        ], className='tab-content')
                    ])
                ]),
                
                dcc.Tab(label='➕ Add New Flight', children=[
                    html.Div([
                        html.Div([
                            html.H3("Add New Flight to System"),
                            html.Div([
                                html.Div([
                                    html.Label("Flight ID", className='form-label'),
                                    dcc.Input(id='add-flight-id', type='text', placeholder='FL001', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Airline Name", className='form-label'),
                                    dcc.Input(id='add-airline', type='text', placeholder='Airline Name', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Flight Number", className='form-label'),
                                    dcc.Input(id='add-flight-number', type='text', placeholder='PK123', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("From City", className='form-label'),
                                    dcc.Input(id='add-from-city', type='text', placeholder='Karachi', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("To City", className='form-label'),
                                    dcc.Input(id='add-to-city', type='text', placeholder='Islamabad', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Departure Time", className='form-label'),
                                    dcc.Input(id='add-dept-time', type='text', placeholder='08:30', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Arrival Time", className='form-label'),
                                    dcc.Input(id='add-arr-time', type='text', placeholder='10:30', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Duration", className='form-label'),
                                    dcc.Input(id='add-duration', type='text', placeholder='2h 00m', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Price (PKR)", className='form-label'),
                                    dcc.Input(id='add-price', type='number', placeholder='15000', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Available Seats", className='form-label'),
                                    dcc.Input(id='add-seats', type='number', placeholder='150', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Aircraft Type", className='form-label'),
                                    dcc.Input(id='add-aircraft', type='text', placeholder='Boeing 737', className='form-input')
                                ], className='form-group'),
                                html.Div(id='add-flight-msg', className='message'),
                                html.Button('ADD FLIGHT', id='add-flight-btn', className='btn-select',
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
                html.H4("About FlightHub"),
                html.Ul([
                    html.Li(html.A("About Us", href="#")),
                    html.Li(html.A("Contact Us", href="#")),
                    html.Li(html.A("Blog", href="#"))
                ])
            ], className='footer-section'),
            html.Div([
                html.H4("Quick Links"),
                html.Ul([
                    html.Li(html.A("Search Flights", href="#")),
                    html.Li(html.A("My Bookings", href="#")),
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
        html.Div("© 2026 FlightHub. All rights reserved. Your trusted partner in flight bookings.", className='footer-bottom')
    ], className='footer')
])

# Callbacks
@callback(
    Output('flights-list', 'children'),
    Input('search-flights-btn', 'n_clicks'),
    State('from-city', 'value'),
    State('to-city', 'value'),
    prevent_initial_call=False
)
def display_flights(n, from_city, to_city):
    try:
        df = pd.read_sql('SELECT * FROM flights', conn)
        if df.empty:
            return html.Div([
                html.Div([
                    html.I(className="fas fa-plane-slash", style={'fontSize': '48px', 'color': '#bdc3c7', 'marginBottom': '10px'}),
                    html.P("No flights available. Add flights to get started!", style={'color': '#7f8c8d', 'fontSize': '16px'})
                ], style={'textAlign': 'center', 'padding': '40px'})
            ])
        
        flights = []
        for _, row in df.iterrows():
            flight = html.Div([
                html.Div([
                    html.Div([
                        html.Div(row['airline'][:2].upper(), className='airline-logo'),
                        html.Div([
                            html.H3(f"{row['airline']} - {row['flight_number']}"),
                            html.P(f"{row['aircraft_type']}")
                        ], className='airline-details')
                    ], className='airline-info'),
                    html.Div([
                        html.Div("PKR ", style={'fontSize': '14px', 'color': '#7f8c8d'}),
                        html.Div(f"{row['price']:,.0f}", className='price')
                    ], className='price-tag')
                ], className='flight-header'),
                
                html.Div([
                    html.Div([
                        html.Div(row['departure_time'], className='flight-time'),
                        html.Div(row['departure_city'], className='flight-city-name')
                    ], className='flight-city'),
                    html.Div([
                        html.I(className="fas fa-arrow-right"),
                        html.Div(row['duration'], className='flight-duration')
                    ], className='flight-arrow'),
                    html.Div([
                        html.Div(row['arrival_time'], className='flight-time'),
                        html.Div(row['arrival_city'], className='flight-city-name')
                    ], className='flight-city')
                ], className='flight-route'),
                
                html.Div([
                    html.Div([
                        html.Div(f"{row['seats_available']}/{row['seats_total']}", className='info-value'),
                        html.Div('Seats Available', className='info-label')
                    ], className='info-item'),
                    html.Div([
                        html.Div("Non-Stop", className='info-value'),
                        html.Div('Flight Type', className='info-label')
                    ], className='info-item'),
                ], className='flight-info'),
                
                html.Div([
                    html.Button('SELECT & BOOK', id={'type': 'select-flight', 'index': row['flight_id']},
                              className='btn-select')
                ], className='flight-actions')
            ], className='flight-card')
            flights.append(flight)
        
        return html.Div(flights)
    except:
        return html.Div("Error loading flights", style={'color': '#c0392b', 'textAlign': 'center', 'padding': '40px'})

@callback(
    Output('add-flight-msg', 'children'),
    Output('add-flight-msg', 'className'),
    Input('add-flight-btn', 'n_clicks'),
    State('add-flight-id', 'value'),
    State('add-airline', 'value'),
    State('add-flight-number', 'value'),
    State('add-from-city', 'value'),
    State('add-to-city', 'value'),
    State('add-dept-time', 'value'),
    State('add-arr-time', 'value'),
    State('add-duration', 'value'),
    State('add-price', 'value'),
    State('add-seats', 'value'),
    State('add-aircraft', 'value'),
    prevent_initial_call=True
)
def add_flight(n, fid, airline, fnumber, from_c, to_c, dept, arr, dur, price, seats, aircraft):
    if all([fid, airline, fnumber, from_c, to_c, dept, arr, dur, price, seats, aircraft]):
        try:
            cursor.execute('''INSERT INTO flights VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                         (fid, airline, fnumber, from_c, to_c, dept, arr, dur, float(price), int(seats), int(seats), aircraft))
            conn.commit()
            return "✅ Flight added successfully!", "message success show"
        except:
            return "❌ Flight ID already exists!", "message error show"
    return "❌ Please fill all fields", "message error show"

@callback(
    Output('booking-msg', 'children'),
    Output('booking-msg', 'className'),
    Input('complete-booking-btn', 'n_clicks'),
    State('book-name', 'value'),
    State('book-email', 'value'),
    State('book-phone', 'value'),
    State('book-flight-id', 'value'),
    State('book-passengers', 'value'),
    prevent_initial_call=True
)
def complete_booking(n, name, email, phone, fid, passengers):
    if all([name, email, phone, fid, passengers]):
        try:
            bid = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute('''INSERT INTO bookings VALUES (?,?,?,?,?,?,?,?)''',
                         (bid, name, email, phone, fid, int(passengers), 
                          datetime.now().strftime('%Y-%m-%d'), 'Confirmed'))
            conn.commit()
            return f"✅ Booking confirmed! Booking ID: {bid}", "message success show"
        except:
            return "❌ Booking failed. Please try again.", "message error show"
    return "❌ Please fill all fields", "message error show"

if __name__ == '__main__':
    app.run(debug=True, port=8050)
