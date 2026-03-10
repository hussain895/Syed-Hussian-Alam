"""
Metro Management System - Animated Visualizer
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np
import time
from datetime import datetime
from metro_system import MetroManagementSystem


class MetroAnimator:
    """Animated visualization for Metro Management System"""

    def __init__(self, metro_system, figsize=(15, 10)):
        self.metro = metro_system
        self.figsize = figsize
        self.fig, self.axes = plt.subplots(2, 2, figsize=figsize)
        self.fig.suptitle('🚇 Metro Management System - Live Animation', fontsize=16, fontweight='bold')

        # Setup subplots
        self.setup_plots()

        # Animation data
        self.frame_count = 0
        self.animation_data = []

    def setup_plots(self):
        """Setup the four subplots"""

        # Top-left: Route visualization
        self.ax_route = self.axes[0, 0]
        self.ax_route.set_title('Metro Route & Trains')
        self.ax_route.set_xlim(-1, 11)
        self.ax_route.set_ylim(-1, 2)
        self.ax_route.axis('off')

        # Top-right: Station status
        self.ax_stations = self.axes[0, 1]
        self.ax_stations.set_title('Station Passenger Queues')
        self.ax_stations.set_xlabel('Stations')
        self.ax_stations.set_ylabel('Passengers Waiting')

        # Bottom-left: Train status
        self.ax_trains = self.axes[1, 0]
        self.ax_trains.set_title('Train Capacities')
        self.ax_trains.set_xlabel('Trains')
        self.ax_trains.set_ylabel('Passengers')

        # Bottom-right: System metrics
        self.ax_metrics = self.axes[1, 1]
        self.ax_metrics.set_title('System Metrics')
        self.ax_metrics.axis('off')

    def draw_route(self):
        """Draw the metro route with stations and trains"""
        self.ax_route.clear()
        self.ax_route.set_title('Metro Route & Trains')
        self.ax_route.set_xlim(-1, 11)
        self.ax_route.set_ylim(-1, 2)
        self.ax_route.axis('off')

        # Get current status
        status = self.metro.get_system_status()
        route = status['route']

        # Draw route line
        x_positions = np.linspace(0, 10, len(route))
        self.ax_route.plot(x_positions, [0] * len(route), 'b-', linewidth=3, alpha=0.7)

        # Draw stations
        station_patches = []
        for i, station in enumerate(route):
            # Station circle
            circle = patches.Circle((x_positions[i], 0), 0.3,
                                  facecolor='lightblue', edgecolor='blue', linewidth=2)
            self.ax_route.add_patch(circle)

            # Station label
            self.ax_route.text(x_positions[i], 0.5, station,
                             ha='center', va='bottom', fontsize=8, rotation=45,
                             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

            # Passenger count at station
            if station in status['stations']:
                waiting = status['stations'][station]['waiting']
                if waiting > 0:
                    self.ax_route.text(x_positions[i], -0.5, f'{waiting} waiting',
                                     ha='center', va='top', fontsize=7, color='red')

        # Draw trains
        for train_id, train_info in status['trains'].items():
            if train_info['location'] in route:
                pos = route.index(train_info['location'])
                x_pos = x_positions[pos]

                # Train rectangle
                train_rect = patches.Rectangle((x_pos-0.2, -0.1), 0.4, 0.2,
                                             facecolor='red', edgecolor='darkred', linewidth=2)
                self.ax_route.add_patch(train_rect)

                # Train label
                passengers = train_info['passengers']
                self.ax_route.text(x_pos, -0.3, f'{train_id}\n({passengers})',
                                 ha='center', va='top', fontsize=7, fontweight='bold')

    def draw_station_status(self):
        """Draw station passenger queue status"""
        self.ax_stations.clear()
        self.ax_stations.set_title('Station Passenger Queues')

        status = self.metro.get_system_status()
        stations = list(status['stations'].keys())
        waiting = [status['stations'][s]['waiting'] for s in stations]
        capacity = [status['stations'][s]['capacity'] for s in stations]

        x = np.arange(len(stations))

        # Capacity bars (background)
        self.ax_stations.bar(x, capacity, alpha=0.3, color='gray', label='Capacity')

        # Waiting passengers bars
        self.ax_stations.bar(x, waiting, color='orange', alpha=0.8, label='Waiting')

        self.ax_stations.set_xticks(x)
        self.ax_stations.set_xticklabels(stations, rotation=45, ha='right')
        self.ax_stations.legend()
        self.ax_stations.grid(True, alpha=0.3)

    def draw_train_status(self):
        """Draw train capacity and load status"""
        self.ax_trains.clear()
        self.ax_trains.set_title('Train Capacities')

        status = self.metro.get_system_status()
        trains = list(status['trains'].keys())
        passengers = [status['trains'][t]['passengers'] for t in trains]
        capacity = [status['trains'][t]['capacity'] for t in trains]

        x = np.arange(len(trains))

        # Capacity bars (background)
        self.ax_trains.bar(x, capacity, alpha=0.3, color='gray', label='Capacity')

        # Current passengers bars
        colors = ['green' if p/c <= 0.8 else 'orange' if p/c <= 0.95 else 'red'
                 for p, c in zip(passengers, capacity)]
        self.ax_trains.bar(x, passengers, color=colors, alpha=0.8, label='Passengers')

        self.ax_trains.set_xticks(x)
        self.ax_trains.set_xticklabels(trains)
        self.ax_trains.legend()
        self.ax_trains.grid(True, alpha=0.3)

    def draw_system_metrics(self):
        """Draw system-wide metrics"""
        self.ax_metrics.clear()
        self.ax_metrics.set_title('System Metrics')
        self.ax_metrics.axis('off')

        status = self.metro.get_system_status()

        # Calculate metrics
        total_waiting = sum(s['waiting'] for s in status['stations'].values())
        total_capacity = sum(s['capacity'] for s in status['stations'].values())
        total_passengers = sum(t['passengers'] for t in status['trains'].values())
        total_train_capacity = sum(t['capacity'] for t in status['trains'].values())

        station_utilization = (total_waiting / total_capacity * 100) if total_capacity > 0 else 0
        train_utilization = (total_passengers / total_train_capacity * 100) if total_train_capacity > 0 else 0

        # Display metrics
        metrics_text = f"""
        System Status - Frame {self.frame_count}

        Stations: {len(status['stations'])}
        • Total Capacity: {total_capacity}
        • Currently Waiting: {total_waiting}
        • Utilization: {station_utilization:.1f}%

        Trains: {len(status['trains'])}
        • Total Capacity: {total_train_capacity}
        • Current Passengers: {total_passengers}
        • Utilization: {train_utilization:.1f}%

        Active Passengers: {status['total_passengers']}
        """

        self.ax_metrics.text(0.05, 0.95, metrics_text,
                           transform=self.ax_metrics.transAxes,
                           fontsize=10, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    def update_frame(self, frame):
        """Update function for animation"""
        self.frame_count = frame

        # Simulate one time step
        self.metro.simulate_time_step()

        # Update all plots
        self.draw_route()
        self.draw_station_status()
        self.draw_train_status()
        self.draw_system_metrics()

        # Store data for analysis
        status = self.metro.get_system_status()
        self.animation_data.append({
            'frame': frame,
            'total_passengers': status['total_passengers'],
            'total_waiting': sum(s['waiting'] for s in status['stations'].values()),
            'total_on_trains': sum(t['passengers'] for t in status['trains'].values())
        })

        return self.ax_route, self.ax_stations, self.ax_trains, self.ax_metrics

    def animate(self, frames=100, interval=1000):
        """Create and run the animation"""
        anim = animation.FuncAnimation(
            self.fig, self.update_frame,
            frames=frames, interval=interval,
            blit=False, repeat=True
        )

        plt.tight_layout()
        return anim

    def save_animation(self, filename='metro_animation.gif', frames=50, interval=500):
        """Save animation to file"""
        anim = self.animate(frames=frames, interval=interval)

        # Save animation
        writer = animation.PillowWriter(fps=2)
        anim.save(filename, writer=writer)
        print(f"Animation saved as {filename}")

        return anim

    def show_static(self):
        """Show a static view of the current system state"""
        self.update_frame(0)
        plt.tight_layout()
        plt.show()

    def get_animation_data(self):
        """Get collected animation data for analysis"""
        return self.animation_data


class MetroSimulationRunner:
    """Runner class for metro simulations with different scenarios"""

    def __init__(self):
        self.metro = MetroManagementSystem()

    def run_peak_hour_simulation(self, frames=50):
        """Simulate peak hour with high passenger volume"""
        print("🏙️ Running Peak Hour Simulation...")

        # Add many passengers at start
        stations = list(self.metro.stations.keys())
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
                "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Parker"]

        for _ in range(20):  # Add 20 passengers
            start = random.choice(stations)
            dest = random.choice([s for s in stations if s != start])
            name = random.choice(names)
            try:
                self.metro.add_passenger(name, start, dest)
            except:
                pass

        # Create animator and run
        animator = MetroAnimator(self.metro)
        anim = animator.animate(frames=frames, interval=800)

        return animator, anim

    def run_emergency_simulation(self, frames=30):
        """Simulate emergency evacuation scenario"""
        print("🚨 Running Emergency Simulation...")

        # Add passengers
        stations = list(self.metro.stations.keys())
        for _ in range(15):
            start = random.choice(stations)
            dest = random.choice([s for s in stations if s != start])
            try:
                self.metro.add_passenger(f"Passenger_{random.randint(100,999)}", start, dest)
            except:
                pass

        # Run normal operation for first half
        animator = MetroAnimator(self.metro)

        def emergency_update(frame):
            if frame == frames // 2:
                # Trigger emergency at random station
                emergency_station = random.choice(stations)
                evacuated = self.metro.emergency_evacuation(emergency_station)
                print(f"🚨 Emergency at {emergency_station}: {evacuated} evacuated")

            return animator.update_frame(frame)

        anim = animation.FuncAnimation(
            animator.fig, emergency_update,
            frames=frames, interval=1000,
            blit=False, repeat=False
        )

        return animator, anim

    def run_capacity_test(self, frames=40):
        """Test system capacity limits"""
        print("📊 Running Capacity Test...")

        # Fill stations to capacity
        stations = list(self.metro.stations.keys())
        passenger_count = 0

        for station in stations:
            capacity = self.metro.stations[station].capacity
            for i in range(capacity + 10):  # Try to exceed capacity
                dest = random.choice([s for s in stations if s != station])
                try:
                    self.metro.add_passenger(f"P{passenger_count}", station, dest)
                    passenger_count += 1
                except OverflowError:
                    break  # Station full

        print(f"Added {passenger_count} passengers to test capacity limits")

        animator = MetroAnimator(self.metro)
        anim = animator.animate(frames=frames, interval=600)

        return animator, anim


def demo_animations():
    """Demonstrate different animation scenarios"""
    print("🎬 Metro Animation Demo")
    print("=" * 50)

    # Peak hour simulation
    print("\n1. Peak Hour Simulation")
    runner = MetroSimulationRunner()
    animator, anim = runner.run_peak_hour_simulation(frames=20)

    # Save animation
    try:
        animator.save_animation('metro_peak_hour.gif', frames=20, interval=800)
    except Exception as e:
        print(f"Could not save animation: {e}")

    # Show static view
    print("\n2. Static System View")
    static_animator = MetroAnimator(MetroManagementSystem())
    static_animator.show_static()

    print("\n✅ Animation demo completed!")


if __name__ == "__main__":
    demo_animations()