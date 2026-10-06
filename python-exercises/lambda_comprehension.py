"""Examples of lambda functions and comprehensions."""

numbers = [1, 2, 3, 4, 5, 6]
square = lambda number: number * number
squares = [square(number) for number in numbers]
even_numbers = [number for number in numbers if number % 2 == 0]

print("Squares:", squares)
print("Even numbers:", even_numbers)