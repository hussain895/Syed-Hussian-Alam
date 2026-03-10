"""
Stack Data Structure Implementation
"""

class Stack:
    """A simple Stack implementation using a list."""
    
    def __init__(self, max_size=None):
        """
        Initialize the stack.
        
        Args:
            max_size: Maximum size of the stack (None for unlimited)
        """
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        """Add an item to the top of the stack."""
        if self.max_size is not None and len(self.items) >= self.max_size:
            raise OverflowError("Stack is full")
        self.items.append(item)
    
    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()
    
    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.items[-1]
    
    def is_empty(self):
        """Check if the stack is empty."""
        return len(self.items) == 0
    
    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)
    
    def __str__(self):
        """String representation of the stack."""
        return f"Stack({self.items})"
    
    def __repr__(self):
        """Detailed representation of the stack."""
        return self.__str__()


if __name__ == "__main__":
    # Example usage
    stack = Stack()
    
    # Push items
    stack.push(10)
    stack.push(20)
    stack.push(30)
    stack.push(40)
    
    print("Stack after pushing:", stack)
    print("Peek:", stack.peek())
    print("Size:", stack.size())
    
    # Pop items
    print("Popped:", stack.pop())
    print("Stack after popping:", stack)
