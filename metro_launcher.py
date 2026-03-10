#!/usr/bin/env python3
"""
Metro Management System - Quick Start Launcher
"""

import os
import sys
import subprocess
import time


def print_banner():
    """Print the metro system banner"""
    banner = """
    🚇 METRO MANAGEMENT SYSTEM 🚇

    A comprehensive metro simulation using Stack & Queue data structures

    Available Options:
    1. Interactive Web Visualizer (Recommended)
    2. Console Demo
    3. Animated Simulations
    4. View Documentation
    5. Exit

    """
    print(banner)


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['dash', 'plotly', 'matplotlib', 'pandas', 'numpy']

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("⚠️  Missing required packages. Installing..."        print(f"Installing: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False

    return True


def run_web_visualizer():
    """Run the interactive web visualizer"""
    print("🌐 Starting Interactive Web Visualizer...")
    print("📱 Open your browser to: http://localhost:8050")
    print("💡 Use Ctrl+C to stop the server")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, 'metro_visualizer.py'])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except FileNotFoundError:
        print("❌ Could not find metro_visualizer.py")
    except Exception as e:
        print(f"❌ Error running visualizer: {e}")


def run_console_demo():
    """Run the console-based demo"""
    print("💻 Running Console Demo...")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, 'metro_system.py'])
    except FileNotFoundError:
        print("❌ Could not find metro_system.py")
    except Exception as e:
        print(f"❌ Error running demo: {e}")


def run_animations():
    """Run the animated simulations"""
    print("🎬 Running Animated Simulations...")
    print("📊 This will create animated visualizations")
    print("-" * 50)

    try:
        subprocess.run([sys.executable, 'metro_animated.py'])
    except FileNotFoundError:
        print("❌ Could not find metro_animated.py")
    except Exception as e:
        print(f"❌ Error running animations: {e}")


def show_documentation():
    """Show the documentation"""
    print("📖 Metro Management System Documentation")
    print("=" * 50)

    try:
        with open('METRO_README.md', 'r') as f:
            content = f.read()
            # Show first 1000 characters
            print(content[:1000])
            print("\n... (truncated)")
            print("\n📄 Full documentation available in METRO_README.md")
    except FileNotFoundError:
        print("❌ Could not find METRO_README.md")
    except Exception as e:
        print(f"❌ Error reading documentation: {e}")


def main():
    """Main launcher function"""
    print_banner()

    # Check dependencies first
    if not check_dependencies():
        print("❌ Dependency check failed. Please resolve and try again.")
        return

    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                run_web_visualizer()
            elif choice == '2':
                run_console_demo()
            elif choice == '3':
                run_animations()
            elif choice == '4':
                show_documentation()
            elif choice == '5':
                print("👋 Thank you for using Metro Management System!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

        print("\n" + "="*50)


if __name__ == "__main__":
    main()