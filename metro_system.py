"""
Metro Management System - Main System
"""

import time
import random
from datetime import datetime, timedelta
from metro_core import Stack, Queue, Passenger, Train, Station


class MetroManagementSystem:
    """Main Metro Management System using Stack and Queue data structures"""

    def __init__(self):
        self.stations = {}
        self.trains = {}
        self.routes = Stack("Metro-Routes")
        self.passenger_history = Stack("Passenger-History")
        self.system_events = Queue("System-Events")
        self.active_passengers = set()

        # Initialize default metro line
        self._initialize_default_line()

    def _initialize_default_line(self):
        """Initialize a default metro line with stations"""
        station_names = [
            "Central Station", "Tech Park", "University", "Shopping Mall",
            "Hospital", "Airport", "Business District", "Residential Area",
            "Sports Complex", "Park Station"
        ]

        # Create stations
        for name in station_names:
            self.add_station(name)

        # Create trains
        for i in range(1, 6):  # 5 trains
            self.add_train(f"T{i:03d}", 150)

        # Set up route (forward direction)
        for station in station_names:
            self.routes.push(station)

    def add_station(self, name, capacity=500):
        """Add a new station to the system"""
        if name not in self.stations:
            self.stations[name] = Station(name, capacity)
            self.system_events.enqueue(f"Station '{name}' added to system")
            return True
        return False

    def add_train(self, train_id, capacity=200):
        """Add a new train to the system"""
        if train_id not in self.trains:
            self.trains[train_id] = Train(train_id, capacity)
            self.system_events.enqueue(f"Train '{train_id}' added to system")
            return True
        return False

    def add_passenger(self, name, start_station, destination_station, ticket_type="regular"):
        """Add a passenger to the system"""
        if start_station not in self.stations or destination_station not in self.stations:
            raise ValueError("Invalid station names")

        passenger_id = f"P{random.randint(1000, 9999)}"
        passenger = Passenger(passenger_id, name, destination_station, ticket_type)

        if self.stations[start_station].add_passenger(passenger):
            self.active_passengers.add(passenger_id)
            self.passenger_history.push(f"Passenger {passenger_id} ({name}) added at {start_station}")
            self.system_events.enqueue(f"Passenger {passenger_id} joined queue at {start_station}")
            return passenger_id
        else:
            raise OverflowError(f"Station {start_station} is at full capacity")

    def operate_train(self, train_id, direction="forward"):
        """Simulate train operation between stations"""
        if train_id not in self.trains:
            raise ValueError(f"Train {train_id} not found")

        train = self.trains[train_id]
        train.direction = direction

        # Get current route
        route_stations = list(self.routes.items)
        if direction == "backward":
            route_stations.reverse()

        current_index = 0
        if train.current_station:
            try:
                current_index = route_stations.index(train.current_station)
            except ValueError:
                current_index = 0

        # Move to next station
        next_index = (current_index + 1) % len(route_stations)
        next_station = route_stations[next_index]

        # Simulate travel
        train.move_to_station(next_station)
        self.system_events.enqueue(f"Train {train_id} arrived at {next_station}")

        # Alight passengers
        alighted = train.alight_passengers(next_station)
        for passenger in alighted:
            self.active_passengers.discard(passenger.id)
            self.passenger_history.push(f"Passenger {passenger.id} arrived at {next_station}")

        # Board new passengers
        if next_station in self.stations:
            boarded = self.stations[next_station].board_passengers(train)
            self.system_events.enqueue(f"{boarded} passengers boarded train {train_id} at {next_station}")

        return {
            "train": train_id,
            "station": next_station,
            "alighted": len(alighted),
            "boarded": boarded,
            "current_load": train.passengers.size()
        }

    def get_system_status(self):
        """Get comprehensive system status"""
        status = {
            "stations": {},
            "trains": {},
            "total_passengers": len(self.active_passengers),
            "system_events": list(self.system_events.items)[-5:],  # Last 5 events
            "route": list(self.routes.items)
        }

        # Station status
        for name, station in self.stations.items():
            status["stations"][name] = {
                "waiting": station.passenger_queue.size(),
                "capacity": station.capacity,
                "utilization": f"{(station.passenger_queue.size() / station.capacity * 100):.1f}%"
            }

        # Train status
        for train_id, train in self.trains.items():
            status["trains"][train_id] = {
                "location": train.current_station or "Depot",
                "passengers": train.passengers.size(),
                "capacity": train.capacity,
                "utilization": f"{(train.passengers.size() / train.capacity * 100):.1f}%",
                "status": train.status
            }

        return status

    def simulate_time_step(self):
        """Simulate one time step of metro operation"""
        # Randomly add passengers
        if random.random() < 0.3:  # 30% chance per step
            stations = list(self.stations.keys())
            start = random.choice(stations)
            destination = random.choice([s for s in stations if s != start])
            names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]

            try:
                passenger_id = self.add_passenger(
                    random.choice(names),
                    start,
                    destination,
                    random.choice(["regular", "student", "senior"])
                )
            except (OverflowError, ValueError):
                pass  # Station full or invalid route

        # Operate trains
        results = []
        for train_id in self.trains.keys():
            if random.random() < 0.7:  # 70% chance trains move
                try:
                    result = self.operate_train(train_id)
                    results.append(result)
                except Exception as e:
                    self.system_events.enqueue(f"Error operating train {train_id}: {str(e)}")

        return results

    def get_passenger_journey(self, passenger_id):
        """Get journey details for a passenger"""
        history = self.passenger_history.get_history()
        journey = [entry for entry in history if passenger_id in entry]
        return journey

    def emergency_evacuation(self, station_name):
        """Handle emergency evacuation at a station"""
        if station_name not in self.stations:
            raise ValueError(f"Station {station_name} not found")

        station = self.stations[station_name]
        evacuated = []

        # Evacuate all waiting passengers
        while not station.passenger_queue.is_empty():
            passenger = station.passenger_queue.dequeue()
            evacuated.append(passenger)
            self.active_passengers.discard(passenger.id)

        # Stop trains at this station
        for train in self.trains.values():
            if train.current_station == station_name:
                train.status = "emergency_stop"

        self.system_events.enqueue(f"EMERGENCY: Evacuated {len(evacuated)} passengers from {station_name}")
        return len(evacuated)

    def reset_system(self):
        """Reset the entire system"""
        self.stations.clear()
        self.trains.clear()
        self.routes.clear()
        self.passenger_history.clear()
        self.system_events.clear()
        self.active_passengers.clear()
        self._initialize_default_line()
        self.system_events.enqueue("System reset completed")


def demo_metro_system():
    """Demonstrate the metro management system"""
    print("🚇 Metro Management System Demo")
    print("=" * 50)

    metro = MetroManagementSystem()

    # Add some passengers
    print("\n📝 Adding passengers...")
    passengers = [
        ("John Doe", "Central Station", "Airport"),
        ("Jane Smith", "Tech Park", "Shopping Mall"),
        ("Bob Johnson", "University", "Business District"),
        ("Alice Brown", "Hospital", "Park Station"),
        ("Charlie Wilson", "Residential Area", "Sports Complex")
    ]

    for name, start, dest in passengers:
        try:
            pid = metro.add_passenger(name, start, dest)
            print(f"✓ Added {name} ({pid}) from {start} to {dest}")
        except Exception as e:
            print(f"✗ Failed to add {name}: {e}")

    # Simulate operations
    print("\n🚂 Simulating train operations...")
    for step in range(5):
        print(f"\n--- Step {step + 1} ---")
        results = metro.simulate_time_step()

        for result in results:
            print(f"Train {result['train']}: {result['station']} | "
                  f"+{result['boarded']} boarded, -{result['alighted']} alighted | "
                  f"Load: {result['current_load']}")

        # Show system status
        status = metro.get_system_status()
        total_waiting = sum(s["waiting"] for s in status["stations"].values())
        print(f"Total passengers waiting: {total_waiting}")

    # Show final status
    print("\n📊 Final System Status:")
    status = metro.get_system_status()
    print(f"Active passengers: {status['total_passengers']}")
    print(f"Stations: {len(status['stations'])}")
    print(f"Trains: {len(status['trains'])}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_metro_system()