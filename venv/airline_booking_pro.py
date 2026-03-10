# Professional Airline Booking System - Bookkaru Style
# Advanced flight booking platform with seat selection and payment

import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go

# External stylesheets
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
]

# Database Setup
conn = sqlite3.connect('airline_booking_pro.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS airlines (
    airline_id TEXT PRIMARY KEY,
    airline_name TEXT,
    logo_url TEXT,
    rating REAL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
    flight_id TEXT PRIMARY KEY,
    airline_id TEXT,
    flight_number TEXT,
    aircraft TEXT,
    departure_city TEXT,
    arrival_city TEXT,
    departure_time TEXT,
    arrival_time TEXT,
    duration TEXT,
    price REAL,
    economy_seats INTEGER,
    business_seats INTEGER,
    economy_available INTEGER,
    business_available INTEGER,
    stops INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS passengers (
    passenger_id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    passport TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    passenger_id TEXT,
    flight_id TEXT,
    seat_class TEXT,
    seats_booked INTEGER,
    total_price REAL,
    booking_date TEXT,
    status TEXT
)''')

conn.commit()

# App Setup
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "FlightBooker - Book Flights Online"

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
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                padding: 15px 0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
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
            
            /* Hero Section */
            .hero {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
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
            }
            
            .hero p {
                font-size: 18px;
                opacity: 0.95;
            }
            
            /* Search Box */
            .search-container {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
                margin: -30px 20px 40px;
                max-width: 1400px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .trip-type {
                display: flex;
                gap: 20px;
                margin-bottom: 25px;
            }
            
            .trip-option {
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
            }
            
            .trip-option input[type="radio"] {
                cursor: pointer;
            }
            
            .search-form {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                align-items: end;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
            }
            
            .form-label {
                font-weight: 600;
                color: #1e3c72;
                margin-bottom: 8px;
                font-size: 13px;
            }
            
            .form-input {
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
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
            
            /* Container */
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
            }
            
            .section-title {
                font-size: 32px;
                font-weight: 700;
                color: #1e3c72;
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
                border-bottom: 1px solid #e0e0e0;
            }
            
            .airline-info {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .airline-logo {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 18px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .airline-details h3 {
                font-size: 16px;
                color: #1e3c72;
                margin-bottom: 3px;
            }
            
            .airline-details p {
                font-size: 12px;
                color: #7f8c8d;
            }
            
            .price-section {
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
            
            .flight-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 20px;
                margin: 15px 0;
                padding: 15px 0;
                border-top: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .detail-item {
                text-align: center;
            }
            
            .detail-time {
                font-size: 18px;
                font-weight: 700;
                color: #1e3c72;
            }
            
            .detail-label {
                font-size: 11px;
                color: #7f8c8d;
                margin-top: 5px;
            }
            
            .flight-features {
                display: flex;
                gap: 15px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            
            .feature-badge {
                background: #f0f0f0;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                color: #555;
            }
            
            .flight-actions {
                display: flex;
                gap: 10px;
                margin-top: 15px;
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
            
            /* Stats Grid */
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
                color: #1e3c72;
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
                color: #1e3c72;
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
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
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
            
            /* Seat Selection */
            .seat-selection {
                background: #f8f9fa;
                padding: 30px;
                border-radius: 12px;
                margin: 20px 0;
            }
            
            .seat-grid {
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                gap: 10px;
                max-width: 400px;
                margin: 20px 0;
            }
            
            .seat {
                width: 40px;
                height: 40px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: 600;
                background: white;
                transition: all 0.3s ease;
            }
            
            .seat:hover {
                border-color: #ff6b35;
            }
            
            .seat.available {
                background: white;
                color: #666;
                border-color: #e0e0e0;
            }
            
            .seat.selected {
                background: #ff6b35;
                color: white;
                border-color: #ff6b35;
            }
            
            .seat.booked {
                background: #ccc;
                color: #999;
                border-color: #ccc;
                cursor: not-allowed;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .hero h1 {
                    font-size: 32px;
                }
                
                .search-form {
                    grid-template-columns: 1fr;
                }
                
                .flight-details {
                    grid-template-columns: repeat(2, 1fr);
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
                html.Span("FlightBooker")
            ], className='navbar-brand'),
            html.Div([
                html.A("Home", href="#", style={'color': 'white'}),
                html.A("Flights", href="#", style={'color': 'white'}),
                html.A("My Bookings", href="#", style={'color': 'white'}),
                html.A("Contact", href="#", style={'color': 'white'}),
            ], className='navbar-menu')
        ], className='navbar-container')
    ], className='navbar'),
    
    # Hero Section
    html.Div([
        html.Div([
            html.H1("BOOK YOUR FLIGHT"),
            html.H1("AT LOWEST PRICES", style={'color': '#ff6b35'}),
            html.P("Find and book flights to anywhere in the world")
        ], className='hero-content')
    ], className='hero'),
    
    # Search Box
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Input(type='radio', id='trip-roundtrip', name='trip-type', value='roundtrip', 
                                 defaultChecked=True, style={'cursor': 'pointer'}),
                        html.Label('Round Trip', htmlFor='trip-roundtrip', style={'cursor': 'pointer', 'marginLeft': '5px'})
                    ], className='trip-option'),
                    html.Div([
                        html.Input(type='radio', id='trip-oneway', name='trip-type', value='oneway', 
                                 style={'cursor': 'pointer'}),
                        html.Label('One Way', htmlFor='trip-oneway', style={'cursor': 'pointer', 'marginLeft': '5px'})
                    ], className='trip-option'),
                    html.Div([
                        html.Input(type='radio', id='trip-multicity', name='trip-type', value='multicity', 
                                 style={'cursor': 'pointer'}),
                        html.Label('Multi-City', htmlFor='trip-multicity', style={'cursor': 'pointer', 'marginLeft': '5px'})
                    ], className='trip-option'),
                ], className='trip-type'),
                
                html.Div([
                    html.Div([
                        html.Label("From", className='form-label'),
                        dcc.Input(id='from-city', type='text', placeholder='Departure City', className='form-input')
                    ], className='form-group'),
                    
                    html.Div([
                        html.Label("To", className='form-label'),
                        dcc.Input(id='to-city', type='text', placeholder='Arrival City', className='form-input')
                    ], className='form-group'),
                    
                    html.Div([
                        html.Label("Departure", className='form-label'),
                        dcc.Input(id='depart-date', type='text', placeholder='YYYY-MM-DD', className='form-input')
                    ], className='form-group'),
                    
                    html.Div([
                        html.Label("Return", className='form-label'),
                        dcc.Input(id='return-date', type='text', placeholder='YYYY-MM-DD', className='form-input')
                    ], className='form-group'),
                    
                    html.Div([
                        html.Label("Passengers", className='form-label'),
                        dcc.Input(id='passengers', type='number', placeholder='1', value=1, className='form-input', min=1)
                    ], className='form-group'),
                    
                    html.Div([
                        html.Label("Class", className='form-label'),
                        dcc.Dropdown(
                            id='seat-class',
                            options=[
                                {'label': 'Economy', 'value': 'economy'},
                                {'label': 'Business', 'value': 'business'}
                            ],
                            value='economy',
                            style={'width': '100%'}
                        )
                    ], className='form-group'),
                    
                    html.Button("SEARCH FLIGHTS", id='search-flights-btn', className='search-btn')
                ], className='search-form')
            ], className='search-container')
        ], className='container')
    ], className='hero', style={'paddingTop': '0', 'paddingBottom': '0'}),
    
    # Main Content
    html.Div([
        # Stats
        html.H2("Book Flights in Easy Steps", className='section-title', style={'marginTop': '40px'}),
        html.Div([
            html.Div([
                html.Div([html.I(className="fas fa-search", style={'fontSize': '32px', 'color': '#ff6b35'})], 
                         style={'fontSize': '32px', 'marginBottom': '10px'}),
                html.Div("Search", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Div("Find your perfect flight", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-chair", style={'fontSize': '32px', 'color': '#ff6b35'})], 
                         style={'fontSize': '32px', 'marginBottom': '10px'}),
                html.Div("Select Seats", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Div("Choose your preferred seats", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-credit-card", style={'fontSize': '32px', 'color': '#ff6b35'})], 
                         style={'fontSize': '32px', 'marginBottom': '10px'}),
                html.Div("Payment", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Div("Complete your payment", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ], className='stat-card'),
            html.Div([
                html.Div([html.I(className="fas fa-check-circle", style={'fontSize': '32px', 'color': '#ff6b35'})], 
                         style={'fontSize': '32px', 'marginBottom': '10px'}),
                html.Div("Confirmation", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Div("Get your booking confirmed", style={'fontSize': '12px', 'color': '#7f8c8d'})
            ], className='stat-card'),
        ], className='stats-grid'),
        
        # Flights List
        html.H2("Available Flights", className='section-title'),
        html.Div(id='flights-list', className='flights-container'),
        
        # Management Tabs
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='✈️ Book Flight', children=[
                    html.Div([
                        html.Div([
                            html.H3("Complete Your Booking"),
                            html.Div([
                                html.Div([
                                    html.Label("Full Name", className='form-label'),
                                    dcc.Input(id='book-name', type='text', placeholder='Enter your full name', className='form-input')
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
                                    html.Label("Passport Number", className='form-label'),
                                    dcc.Input(id='book-passport', type='text', placeholder='Enter passport number', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Flight ID", className='form-label'),
                                    dcc.Input(id='book-flight-id', type='text', placeholder='Select a flight', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Seat Class", className='form-label'),
                                    dcc.Dropdown(
                                        id='book-seat-class',
                                        options=[
                                            {'label': 'Economy', 'value': 'economy'},
                                            {'label': 'Business', 'value': 'business'}
                                        ],
                                        value='economy',
                                        style={'width': '100%'}
                                    )
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Number of Seats", className='form-label'),
                                    dcc.Input(id='book-seats', type='number', value=1, className='form-input', min=1)
                                ], className='form-group'),
                                html.Div(id='booking-msg', className='message'),
                                html.Button('COMPLETE BOOKING', id='complete-booking-btn', className='btn-select', 
                                          style={'background': 'linear-gradient(135deg, #ff6b35 0%, #ff5722 100%)', 'marginTop': '10px'})
                            ], className='form-section')
                        ], className='tab-content')
                    ])
                ]),
                
                dcc.Tab(label='➕ Add Flight', children=[
                    html.Div([
                        html.Div([
                            html.H3("Add New Flight"),
                            html.Div([
                                html.Div([
                                    html.Label("Flight ID", className='form-label'),
                                    dcc.Input(id='add-flight-id', type='text', placeholder='FL001', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Airline", className='form-label'),
                                    dcc.Input(id='add-airline', type='text', placeholder='Airline Name', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Flight Number", className='form-label'),
                                    dcc.Input(id='add-flight-number', type='text', placeholder='PK123', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Aircraft", className='form-label'),
                                    dcc.Input(id='add-aircraft', type='text', placeholder='Boeing 777', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("From City", className='form-label'),
                                    dcc.Input(id='add-from', type='text', placeholder='Karachi', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("To City", className='form-label'),
                                    dcc.Input(id='add-to', type='text', placeholder='Islamabad', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Departure Time", className='form-label'),
                                    dcc.Input(id='add-dept', type='text', placeholder='HH:MM', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Arrival Time", className='form-label'),
                                    dcc.Input(id='add-arr', type='text', placeholder='HH:MM', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Duration", className='form-label'),
                                    dcc.Input(id='add-duration', type='text', placeholder='2h 30m', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Price (PKR)", className='form-label'),
                                    dcc.Input(id='add-price', type='number', placeholder='25000', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Economy Seats", className='form-label'),
                                    dcc.Input(id='add-economy', type='number', placeholder='180', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Business Seats", className='form-label'),
                                    dcc.Input(id='add-business', type='number', placeholder='30', className='form-input')
                                ], className='form-group'),
                                html.Div([
                                    html.Label("Stops", className='form-label'),
                                    dcc.Input(id='add-stops', type='number', placeholder='0', className='form-input', min=0)
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
                html.H4("About FlightBooker"),
                html.Ul([
                    html.Li(html.A("About Us", href="#")),
                    html.Li(html.A("Contact", href="#")),
                    html.Li(html.A("Blog", href="#"))
                ])
            ], className='footer-section'),
            html.Div([
                html.H4("Quick Links"),
                html.Ul([
                    html.Li(html.A("Search Flights", href="#")),
                    html.Li(html.A("My Bookings", href="#")),
                    html.Li(html.A("FAQ", href="#"))
                ])
            ], className='footer-section'),
            html.Div([
                html.H4("Support"),
                html.Ul([
                    html.Li(html.A("Help Center", href="#")),
                    html.Li(html.A("Contact Support", href="#")),
                    html.Li(html.A("Live Chat", href="#"))
                ])
            ], className='footer-section'),
        ], className='footer-content'),
        html.Div("© 2026 FlightBooker. All rights reserved.", className='footer-bottom')
    ], className='footer')
])

# Callbacks
@callback(
    Output('flights-list', 'children'),
    Input('search-flights-btn', 'n_clicks'),
    prevent_initial_call=False
)
def display_flights(n):
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
                        html.Div(row['airline_id'][:2].upper(), className='airline-logo'),
                        html.Div([
                            html.H3(f"{row['airline_id']} - {row['flight_number']}"),
                            html.P(f"{row['aircraft']}")
                        ], className='airline-details')
                    ], className='airline-info'),
                    html.Div([
                        html.Div("PKR", style={'fontSize': '14px', 'color': '#7f8c8d'}),
                        html.Div(f"{row['price']:,.0f}", className='price')
                    ], className='price-section')
                ], className='flight-header'),
                
                html.Div([
                    html.Div([
                        html.Div(row['departure_time'], className='detail-time'),
                        html.Div(row['departure_city'], className='detail-label')
                    ], className='detail-item'),
                    html.Div([
                        html.Div(f"✈️ {row['duration']}", className='detail-time'),
                        html.Div(f"{row['stops']} Stop{'s' if row['stops'] != 1 else ''}", className='detail-label')
                    ], className='detail-item'),
                    html.Div([
                        html.Div(row['arrival_time'], className='detail-time'),
                        html.Div(row['arrival_city'], className='detail-label')
                    ], className='detail-item')
                ], className='flight-details'),
                
                html.Div([
                    html.Div("✓ Free Baggage", className='feature-badge'),
                    html.Div("✓ Free Meal", className='feature-badge'),
                    html.Div(f"✓ {row['economy_available']} Eco Seats", className='feature-badge'),
                    html.Div(f"✓ {row['business_available']} Bus Seats", className='feature-badge'),
                ], className='flight-features'),
                
                html.Div([
                    html.Button('SELECT FLIGHT', id={'type': 'select-flight', 'index': row['flight_id']},
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
    State('add-aircraft', 'value'),
    State('add-from', 'value'),
    State('add-to', 'value'),
    State('add-dept', 'value'),
    State('add-arr', 'value'),
    State('add-duration', 'value'),
    State('add-price', 'value'),
    State('add-economy', 'value'),
    State('add-business', 'value'),
    State('add-stops', 'value'),
    prevent_initial_call=True
)
def add_flight(n, fid, airline, fnumber, aircraft, from_c, to_c, dept, arr, dur, price, eco, bus, stops):
    if all([fid, airline, fnumber, aircraft, from_c, to_c, dept, arr, dur, price, eco, bus]):
        try:
            cursor.execute('''INSERT INTO flights VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                         (fid, airline, fnumber, aircraft, from_c, to_c, dept, arr, dur, float(price),
                          int(eco), int(bus), int(eco), int(bus), int(stops) if stops else 0))
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
    State('book-passport', 'value'),
    State('book-flight-id', 'value'),
    State('book-seat-class', 'value'),
    State('book-seats', 'value'),
    prevent_initial_call=True
)
def complete_booking(n, name, email, phone, passport, fid, seat_class, seats):
    if all([name, email, phone, passport, fid, seats]):
        try:
            pid = f"PAX{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute('''INSERT INTO passengers VALUES (?,?,?,?,?)''',
                         (pid, name, email, phone, passport))
            conn.commit()
            
            bid = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
            cursor.execute('SELECT price FROM flights WHERE flight_id = ?', (fid,))
            price_result = cursor.fetchone()
            total_price = (price_result[0] * int(seats)) if price_result else 0
            
            cursor.execute('''INSERT INTO bookings VALUES (?,?,?,?,?,?,?,?)''',
                         (bid, pid, fid, seat_class, int(seats), total_price,
                          datetime.now().strftime('%Y-%m-%d'), 'Confirmed'))
            conn.commit()
            return f"✅ Booking confirmed! ID: {bid}", "message success show"
        except Exception as e:
            return f"❌ Booking failed: {str(e)}", "message error show"
    return "❌ Please fill all fields", "message error show"

if __name__ == '__main__':
    app.run(debug=True, port=8050)
