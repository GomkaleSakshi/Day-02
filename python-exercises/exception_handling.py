"""Handle common errors while converting user input."""

try:
    age_text = input("Enter your age: ").strip()
    if not age_text:
        raise ValueError("Age cannot be empty.")
    age = int(age_text)
    if age < 0:
        raise ValueError("Age cannot be negative.")
except ValueError as error:
    print("Please enter a valid age:", error)
else:
    print("Next year you will be", age + 1)