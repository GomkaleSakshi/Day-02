"""A JSON-backed, menu-driven employee management system."""

import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("data.json")


class EmployeeNotFoundError(Exception):
    """Raised when an employee ID does not exist."""


class DuplicateEmployeeError(Exception):
    """Raised when an employee ID is already in use."""


def load_employees():
    """Load employee records, using an empty list for missing or invalid data."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as data_file:
            employees = json.load(data_file)
        if not isinstance(employees, list):
            raise ValueError("The JSON root must be a list of employees.")
        return employees
    except FileNotFoundError:
        print("Data file not found. Starting with an empty employee list.")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON in {DATA_FILE.name}: {error}. Starting with an empty list.")
    except (OSError, ValueError) as error:
        print(f"Could not read employee data: {error}. Starting with an empty list.")
    return []


def save_employees(employees):
    """Save employee records as readable JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as data_file:
            json.dump(employees, data_file, indent=4)
        return True
    except OSError as error:
        print(f"Could not save employee data: {error}")
        return False


def find_employee(employees, employee_id):
    """Return the employee with the requested ID."""
    for employee in employees:
        if employee.get("id") == employee_id:
            return employee
    raise EmployeeNotFoundError(f"No employee found with ID {employee_id}.")


def read_required_text(prompt):
    """Read a non-empty value from the user."""
    value = input(prompt).strip()
    if not value:
        raise ValueError("This field cannot be empty.")
    return value


def read_salary(prompt="Salary: "):
    """Read a valid, non-negative salary."""
    salary_text = read_required_text(prompt)
    try:
        salary = float(salary_text)
    except ValueError as error:
        raise ValueError("Salary must be a valid number.") from error
    if salary < 0:
        raise ValueError("Salary cannot be negative.")
    return salary


def read_age(prompt="Age: "):
    """Read a valid, positive employee age."""
    age_text = read_required_text(prompt)
    try:
        age = int(age_text)
    except ValueError as error:
        raise ValueError("Age must be a whole number.") from error
    if age <= 0:
        raise ValueError("Age must be greater than zero.")
    return age


def add_employee(employees):
    """Collect and save a new employee."""
    employee_id = read_required_text("Employee ID: ")
    if any(employee.get("id") == employee_id for employee in employees):
        raise DuplicateEmployeeError(f"Employee ID {employee_id} already exists.")
    employee = {
        "id": employee_id,
        "name": read_required_text("Name: "),
        "department": read_required_text("Department: "),
        "salary": read_salary(),
        "age": read_age(),
    }
    employees.append(employee)
    if save_employees(employees):
        print("Employee added successfully.")
    else:
        employees.pop()


def update_employee(employees):
    """Update an existing employee; blank fields keep their current values."""
    employee_id = read_required_text("Employee ID to update: ")
    employee = find_employee(employees, employee_id)
    print("Press Enter to keep the current value.")
    name = input(f"Name [{employee['name']}]: ").strip()
    department = input(f"Department [{employee['department']}]: ").strip()
    salary_text = input(f"Salary [{employee['salary']}]: ").strip()
    age_text = input(f"Age [{employee['age']}]: ").strip()

    updated = employee.copy()
    if name:
        updated["name"] = name
    if department:
        updated["department"] = department
    if salary_text:
        try:
            updated["salary"] = float(salary_text)
        except ValueError as error:
            raise ValueError("Salary must be a valid number.") from error
        if updated["salary"] < 0:
            raise ValueError("Salary cannot be negative.")
    if age_text:
        try:
            updated["age"] = int(age_text)
        except ValueError as error:
            raise ValueError("Age must be a whole number.") from error
        if updated["age"] <= 0:
            raise ValueError("Age must be greater than zero.")

    original = employee.copy()
    employee.update(updated)
    if save_employees(employees):
        print("Employee updated successfully.")
    else:
        employee.update(original)


def delete_employee(employees):
    """Delete an employee by ID and save the updated list."""
    employee_id = read_required_text("Employee ID to delete: ")
    employee = find_employee(employees, employee_id)
    employees.remove(employee)
    if save_employees(employees):
        print("Employee deleted successfully.")
    else:
        employees.append(employee)


def display_employees(employees):
    """Display employees in aligned columns."""
    if not employees:
        print("No employees to display.")
        return
    print(f"{'ID':<12} {'Name':<22} {'Department':<18} {'Salary':>12} {'Age':>5}")
    print("-" * 73)
    for employee in employees:
        print(
            f"{employee['id']:<12} {employee['name']:<22} "
            f"{employee['department']:<18} {employee['salary']:>12.2f} "
            f"{employee['age']:>5}"
        )


def search_employees(employees):
    """Search by exact ID or partial, case-insensitive name."""
    query = read_required_text("Enter an employee ID or name: ").casefold()
    matches = [
        employee
        for employee in employees
        if employee.get("id", "").casefold() == query
        or query in employee.get("name", "").casefold()
    ]
    display_employees(matches)


def filter_employees(employees):
    """Filter by department or by an inclusive salary range."""
    print("1. Department\n2. Salary range")
    choice = read_required_text("Choose a filter: ")
    if choice == "1":
        department = read_required_text("Department: ").casefold()
        matches = [
            employee for employee in employees
            if employee.get("department", "").casefold() == department
        ]
    elif choice == "2":
        minimum = read_salary("Minimum salary: ")
        maximum = read_salary("Maximum salary: ")
        if minimum > maximum:
            raise ValueError("Minimum salary cannot be greater than maximum salary.")
        matches = [
            employee for employee in employees
            if minimum <= employee.get("salary", 0) <= maximum
        ]
    else:
        raise ValueError("Choose 1 or 2.")
    display_employees(matches)


def sort_employees(employees):
    """Display employees sorted by name, salary, or age."""
    sort_fields = {"1": ("name", "name"), "2": ("salary", "salary"), "3": ("age", "age")}
    print("1. Name\n2. Salary\n3. Age")
    choice = read_required_text("Sort by: ")
    if choice not in sort_fields:
        raise ValueError("Choose 1, 2, or 3.")
    field, label = sort_fields[choice]
    direction = read_required_text("Order (A)scending or (D)escending: ").casefold()
    if direction not in ("a", "ascending", "d", "descending"):
        raise ValueError("Enter A for ascending or D for descending.")
    sorted_employees = sorted(
        employees,
        key=lambda employee: employee.get(field, "").casefold()
        if label == "name"
        else employee.get(field, 0),
        reverse=direction in ("d", "descending"),
    )
    display_employees(sorted_employees)


def show_statistics(employees):
    """Display salary and department statistics."""
    if not employees:
        print("No employee data is available for statistics.")
        return
    salaries = [employee["salary"] for employee in employees]
    department_counts = {}
    for employee in employees:
        department = employee["department"]
        department_counts[department] = department_counts.get(department, 0) + 1
    print("Total employees:", len(employees))
    print(f"Average salary: {sum(salaries) / len(salaries):.2f}")
    print(f"Minimum salary: {min(salaries):.2f}")
    print(f"Maximum salary: {max(salaries):.2f}")
    print("Department-wise employee count:")
    for department, count in sorted(department_counts.items()):
        print(f"  {department}: {count}")


def display_menu():
    print("\nEmployee Management System")
    print("1. Add Employee")
    print("2. Update Employee")
    print("3. Delete Employee")
    print("4. Search Employee")
    print("5. Filter Employees")
    print("6. Sort Employees")
    print("7. Statistics")
    print("8. Display All Employees")
    print("9. Exit")


def main():
    employees = load_employees()
    actions = {
        "1": add_employee,
        "2": update_employee,
        "3": delete_employee,
        "4": search_employees,
        "5": filter_employees,
        "6": sort_employees,
        "7": show_statistics,
        "8": display_employees,
    }
    while True:
        display_menu()
        try:
            choice = input("Choose an option (1-9): ").strip()
            if choice == "9":
                print("Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Please choose a number from 1 to 9.")
                continue
            action(employees)
        except (ValueError, EmployeeNotFoundError, DuplicateEmployeeError) as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print("\nApplication closed.")
            break
        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()