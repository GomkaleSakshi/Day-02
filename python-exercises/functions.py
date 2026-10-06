"""Defining and calling simple functions."""


def calculate_total(price, quantity):
    """Return the cost of a quantity of items."""
    return price * quantity


def greet(name):
    """Return a friendly greeting."""
    return f"Hello, {name}!"


print(greet("Asha"))
print("Order total:", calculate_total(12.5, 3))