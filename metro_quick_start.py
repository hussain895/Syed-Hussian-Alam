#!/usr/bin/env python3
"""
Metro Management System - Quick Start Script
Automatically sets up and runs the metro management system
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")

    required_packages = ['dash', 'pandas']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} is missing")

    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False

    return True

def setup_database():
    """Set up the database with sample data"""
    print("\n🗄️  Setting up database...")

    try:
        # Run the sample data script
        result = subprocess.run([sys.executable, 'metro_sample_data.py'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Database setup completed!")
            print(result.stdout)
            return True
        else:
            print("❌ Database setup failed!")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("❌ Sample data script not found!")
        return False

def start_application():
    """Start the Metro Management System"""
    print("\n🚀 Starting Metro Management System...")

    try:
        print("📱 Opening web interface at: http://localhost:8050")
        print("💡 Press Ctrl+C to stop the server")
        print("\n" + "="*50)

        # Start the application
        subprocess.run([sys.executable, 'metro_management_system.py'])

    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def show_welcome():
    """Show welcome message and instructions"""
    print("🚇 Metro Management System - Quick Start")
    print("=" * 50)
    print("Welcome to MetroHub - Your Metro Ticket Booking System!")
    print("\nThis script will:")
    print("   1. Check and install required dependencies")
    print("   2. Set up the database with sample routes")
    print("   3. Start the web application")
    print("\nLet's get started!")
    print("=" * 50)

def show_completion():
    """Show completion message"""
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\n📋 What you can do now:")
    print("   • Book metro tickets online")
    print("   • Add new routes to the system")
    print("   • View available routes and schedules")
    print("   • Manage passenger bookings")
    print("\n📖 For more information, see: METRO_MANAGEMENT_README.md")
    print("\n🚀 Happy metro traveling!")
    print("=" * 50)

def main():
    """Main setup function"""
    show_welcome()

    # Check if we're in the right directory
    if not os.path.exists('metro_management_system.py'):
        print("❌ Error: metro_management_system.py not found in current directory")
        print("   Please run this script from the MetroHub directory")
        return

    # Check dependencies
    if not check_dependencies():
        return

    # Setup database
    if not setup_database():
        return

    # Show completion message
    show_completion()

    # Wait a moment before starting
    print("\n⏳ Starting web application in 3 seconds...")
    time.sleep(3)

    # Start the application
    start_application()

if __name__ == "__main__":
    main()