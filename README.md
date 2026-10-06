# Day-02 Python Development Practical

## Objective

Practice core Python concepts and build a JSON-backed Employee Management System and a CSV analysis program using the Python standard library.

## Technologies Used

- Python 3
- JSON and CSV file formats
- Python standard library only

## Project Structure

```text
Day-02/
├── python-exercises/
│   ├── variables.py
│   ├── lists_tuples_sets_dictionary.py
│   ├── conditions_loops.py
│   ├── functions.py
│   ├── lambda_comprehension.py
│   ├── modules_packages.py
│   ├── exception_handling.py
│   ├── file_handling.py
│   └── classes_objects.py
├── management-system/
│   ├── management.py
│   └── data.json
├── csv-analysis/
│   ├── analysis.py
│   └── employees.csv
└── README.md
```

## Features

- Runnable examples for variables and data types, collections, conditions, loops, functions, lambda functions, comprehensions, modules, exceptions, files, classes, objects, inheritance, and encapsulation.
- Employee records are stored as JSON beside the management script.
- Employee CSV summaries are calculated with Python's built-in `csv` module.

## Management System Features

- Add, update, and delete employees with JSON persistence.
- Search by employee ID or partial name.
- Filter by department or salary range.
- Sort by name, salary, or age in ascending or descending order.
- View total employees, average/minimum/maximum salary, and department counts.
- Display employee records in aligned columns.
- Validate unique IDs, required text fields, salary, and age.

Employee fields are ID, Name, Department, Salary, and Age. IDs are treated as text; salary must be non-negative and age must be a positive whole number.

## CSV Analysis Features

- Counts employee records, missing cells, and duplicate records.
- Reports average, minimum, and maximum valid salary.
- Reports employee counts and average salary by department.
- Skips malformed salary values and reports how many were skipped.

## How to Run

Open the `Day-02` folder in VS Code and use its integrated terminal. Python 3 must be installed and available as `python` on the PATH.

```powershell
python management-system/management.py
python csv-analysis/analysis.py
python python-exercises/variables.py
```

Run any other exercise with the same pattern, replacing the script name. The programs resolve their data files relative to their own script folders, so the commands work from the project root.

## Sample Menu

```text
Employee Management System
1. Add Employee
2. Update Employee
3. Delete Employee
4. Search Employee
5. Filter Employees
6. Sort Employees
7. Statistics
8. Display All Employees
9. Exit
Choose an option (1-9):
```

## Sample Output

The CSV analysis for the included sample data begins like this:

```text
Total record count: 10
Missing values: 0
Duplicate records: 0
Average salary: 68600.00
Minimum salary: 58000.00
Maximum salary: 81000.00
Department-wise employee count:
  Finance: 2
  HR: 2
  IT: 3
  Sales: 3
```

## Exception Handling

- Empty required fields and invalid salary or age inputs are rejected with a clear message.
- Duplicate IDs and missing employee IDs are reported without terminating the menu.
- Missing, unreadable, or invalid JSON files are handled; the program starts with an empty list when the stored data cannot be loaded.
- File save and CSV read errors are displayed to the user.
- Missing CSV cells, duplicate rows, and invalid salary values are included in the analysis or reported.
- End-of-file input and Ctrl+C close the management menu cleanly.