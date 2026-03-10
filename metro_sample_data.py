#!/usr/bin/env python3
"""
Metro Management System - Sample Data Generator
Populates the database with sample metro routes for testing
"""

import sqlite3
from datetime import datetime, timedelta

def create_sample_data():
    """Create and populate sample metro routes"""

    # Connect to database
    conn = sqlite3.connect('metro_management.db')
    cursor = conn.cursor()

    # Sample metro routes data
    sample_routes = [
        {
            'route_id': 'RT001',
            'metro_line': 'Red Line',
            'route_number': 'R001',
            'departure_station': 'Central Station',
            'arrival_station': 'Airport Station',
            'departure_time': '08:30',
            'arrival_time': '09:15',
            'duration': '45 mins',
            'fare': 150.0,
            'seats_available': 200,
            'seats_total': 200,
            'train_type': 'Express Train'
        },
        {
            'route_id': 'RT002',
            'metro_line': 'Red Line',
            'route_number': 'R002',
            'departure_station': 'Central Station',
            'arrival_station': 'Mall Station',
            'departure_time': '09:00',
            'arrival_time': '09:20',
            'duration': '20 mins',
            'fare': 80.0,
            'seats_available': 180,
            'seats_total': 180,
            'train_type': 'Local Train'
        },
        {
            'route_id': 'RT003',
            'metro_line': 'Blue Line',
            'route_number': 'B001',
            'departure_station': 'Downtown Station',
            'arrival_station': 'University Station',
            'departure_time': '09:00',
            'arrival_time': '09:30',
            'duration': '30 mins',
            'fare': 100.0,
            'seats_available': 150,
            'seats_total': 150,
            'train_type': 'Express Train'
        },
        {
            'route_id': 'RT004',
            'metro_line': 'Blue Line',
            'route_number': 'B002',
            'departure_station': 'Downtown Station',
            'arrival_station': 'Hospital Station',
            'departure_time': '09:15',
            'arrival_time': '09:45',
            'duration': '30 mins',
            'fare': 90.0,
            'seats_available': 160,
            'seats_total': 160,
            'train_type': 'Local Train'
        },
        {
            'route_id': 'RT005',
            'metro_line': 'Green Line',
            'route_number': 'G001',
            'departure_station': 'North Station',
            'arrival_station': 'South Station',
            'departure_time': '08:45',
            'arrival_time': '09:30',
            'duration': '45 mins',
            'fare': 120.0,
            'seats_available': 190,
            'seats_total': 190,
            'train_type': 'Express Train'
        },
        {
            'route_id': 'RT006',
            'metro_line': 'Green Line',
            'route_number': 'G002',
            'departure_station': 'North Station',
            'arrival_station': 'Park Station',
            'departure_time': '09:30',
            'arrival_time': '09:50',
            'duration': '20 mins',
            'fare': 70.0,
            'seats_available': 170,
            'seats_total': 170,
            'train_type': 'Local Train'
        },
        {
            'route_id': 'RT007',
            'metro_line': 'Yellow Line',
            'route_number': 'Y001',
            'departure_station': 'East Station',
            'arrival_station': 'West Station',
            'departure_time': '08:00',
            'arrival_time': '08:40',
            'duration': '40 mins',
            'fare': 110.0,
            'seats_available': 175,
            'seats_total': 175,
            'train_type': 'Express Train'
        },
        {
            'route_id': 'RT008',
            'metro_line': 'Orange Line',
            'route_number': 'O001',
            'departure_station': 'Industrial Station',
            'arrival_station': 'Business District',
            'departure_time': '07:30',
            'arrival_time': '08:15',
            'duration': '45 mins',
            'fare': 130.0,
            'seats_available': 185,
            'seats_total': 185,
            'train_type': 'Express Train'
        }
    ]

    # Insert sample routes
    for route in sample_routes:
        try:
            cursor.execute('''INSERT INTO metro_routes VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                         (route['route_id'], route['metro_line'], route['route_number'],
                          route['departure_station'], route['arrival_station'],
                          route['departure_time'], route['arrival_time'], route['duration'],
                          route['fare'], route['seats_available'], route['seats_total'],
                          route['train_type']))
            print(f"✅ Added route: {route['route_id']} - {route['metro_line']} ({route['departure_station']} → {route['arrival_station']})")
        except sqlite3.IntegrityError:
            print(f"⚠️  Route {route['route_id']} already exists, skipping...")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n🎉 Sample data generation completed!")
    print(f"📊 Added {len(sample_routes)} metro routes to the database")
    print("\n🚀 You can now run the Metro Management System!")

def show_database_stats():
    """Show current database statistics"""

    conn = sqlite3.connect('metro_management.db')
    cursor = conn.cursor()

    # Count routes
    cursor.execute('SELECT COUNT(*) FROM metro_routes')
    route_count = cursor.fetchone()[0]

    # Count bookings
    cursor.execute('SELECT COUNT(*) FROM ticket_bookings')
    booking_count = cursor.fetchone()[0]

    # Show route details
    if route_count > 0:
        print(f"\n📊 Database Statistics:")
        print(f"   Routes: {route_count}")
        print(f"   Bookings: {booking_count}")

        print(f"\n🛤️ Available Routes:")
        cursor.execute('SELECT route_id, metro_line, departure_station, arrival_station, fare FROM metro_routes ORDER BY metro_line, route_id')
        routes = cursor.fetchall()

        current_line = None
        for route in routes:
            if route[1] != current_line:
                current_line = route[1]
                print(f"\n   {current_line}:")
            print(f"     {route[0]}: {route[2]} → {route[3]} (PKR {route[4]:.0f})")

    conn.close()

if __name__ == "__main__":
    print("🚇 Metro Management System - Sample Data Generator")
    print("=" * 55)

    # Create sample data
    create_sample_data()

    # Show statistics
    show_database_stats()

    print("\n" + "=" * 55)
    print("🎯 Next Steps:")
    print("   1. Run: python metro_management_system.py")
    print("   2. Open: http://localhost:8050")
    print("   3. Start booking metro tickets!")
    print("=" * 55)