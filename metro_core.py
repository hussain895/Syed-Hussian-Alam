"""
Metro Management System - Core Data Structures
"""

from collections import deque
import time
from datetime import datetime, timedelta


class Stack:
    """Enhanced Stack implementation for Metro Management"""

    def __init__(self, name="Stack", max_size=None):
        self.items = []
        self.max_size = max_size
        self.name = name
        self.operation_history = []

    def push(self, item):
        """Add an item to the top of the stack."""
        if self.max_size is not None and len(self.items) >= self.max_size:
            raise OverflowError(f"{self.name} is full")
        self.items.append(item)
        self.operation_history.append(f"PUSH: {item} at {datetime.now().strftime('%H:%M:%S')}")

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError(f"{self.name} is empty")
        item = self.items.pop()
        self.operation_history.append(f"POP: {item} at {datetime.now().strftime('%H:%M:%S')}")
        return item

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError(f"{self.name} is empty")
        return self.items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)

    def clear(self):
        """Clear all items from the stack."""
        self.items.clear()
        self.operation_history.append(f"CLEAR: All items removed at {datetime.now().strftime('%H:%M:%S')}")

    def get_history(self):
        """Get operation history."""
        return self.operation_history[-10:]  # Last 10 operations

    def __str__(self):
        return f"{self.name}({self.items})"


class Queue:
    """Queue implementation using deque for passenger management"""

    def __init__(self, name="Queue", max_size=None):
        self.items = deque()
        self.max_size = max_size
        self.name = name
        self.operation_history = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        if self.max_size is not None and len(self.items) >= self.max_size:
            raise OverflowError(f"{self.name} is full")
        self.items.append(item)
        self.operation_history.append(f"ENQUEUE: {item} at {datetime.now().strftime('%H:%M:%S')}")

    def dequeue(self):
        """Remove and return the front item from the queue."""
        if self.is_empty():
            raise IndexError(f"{self.name} is empty")
        item = self.items.popleft()
        self.operation_history.append(f"DEQUEUE: {item} at {datetime.now().strftime('%H:%M:%S')}")
        return item

    def peek(self):
        """Return the front item without removing it."""
        if self.is_empty():
            raise IndexError(f"{self.name} is empty")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()
        self.operation_history.append(f"CLEAR: All items removed at {datetime.now().strftime('%H:%M:%S')}")

    def get_history(self):
        return self.operation_history[-10:]

    def __str__(self):
        return f"{self.name}({list(self.items)})"


class Passenger:
    """Represents a metro passenger"""

    def __init__(self, passenger_id, name, destination, ticket_type="regular"):
        self.id = passenger_id
        self.name = name
        self.destination = destination
        self.ticket_type = ticket_type
        self.boarding_time = None
        self.alighting_time = None
        self.status = "waiting"  # waiting, boarded, arrived

    def board_train(self, station):
        self.boarding_time = datetime.now()
        self.status = "boarded"

    def alight_train(self, station):
        self.alighting_time = datetime.now()
        self.status = "arrived"

    def __str__(self):
        return f"Passenger({self.id}: {self.name} -> {self.destination})"


class Train:
    """Represents a metro train"""

    def __init__(self, train_id, capacity=200):
        self.id = train_id
        self.capacity = capacity
        self.passengers = Stack(f"Train-{train_id}-Passengers", capacity)
        self.current_station = None
        self.direction = "forward"  # forward, backward
        self.status = "stationary"  # stationary, moving, maintenance
        self.route_history = []

    def board_passenger(self, passenger):
        """Board a passenger onto the train"""
        if self.passengers.size() < self.capacity:
            self.passengers.push(passenger)
            passenger.board_train(self.current_station)
            return True
        return False

    def alight_passengers(self, station):
        """Alight passengers at destination station"""
        alighted = []
        temp_stack = Stack("Temp")

        # Check all passengers for this destination
        while not self.passengers.is_empty():
            passenger = self.passengers.pop()
            if passenger.destination == station:
                passenger.alight_train(station)
                alighted.append(passenger)
            else:
                temp_stack.push(passenger)

        # Put back passengers who didn't alight
        while not temp_stack.is_empty():
            self.passengers.push(temp_stack.pop())

        return alighted

    def move_to_station(self, station):
        """Move train to a new station"""
        self.current_station = station
        self.route_history.append(f"{station} at {datetime.now().strftime('%H:%M:%S')}")
        self.status = "moving"

    def __str__(self):
        return f"Train({self.id}): {self.passengers.size()}/{self.capacity} passengers at {self.current_station}"


class Station:
    """Represents a metro station"""

    def __init__(self, name, capacity=500):
        self.name = name
        self.capacity = capacity
        self.passenger_queue = Queue(f"{name}-Queue", capacity)
        self.platforms = {}  # platform_id -> train
        self.connected_stations = []

    def add_passenger(self, passenger):
        """Add passenger to station queue"""
        if self.passenger_queue.size() < self.capacity:
            self.passenger_queue.enqueue(passenger)
            return True
        return False

    def board_passengers(self, train, max_board=50):
        """Board passengers onto train"""
        boarded = 0
        while (not self.passenger_queue.is_empty() and
               train.passengers.size() < train.capacity and
               boarded < max_board):
            passenger = self.passenger_queue.dequeue()
            if train.board_passenger(passenger):
                boarded += 1
        return boarded

    def __str__(self):
        return f"Station({self.name}): {self.passenger_queue.size()}/{self.capacity} waiting"