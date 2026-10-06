"""Summarize employee data from the adjacent CSV file."""

import csv
from collections import Counter, defaultdict
from pathlib import Path


CSV_FILE = Path(__file__).with_name("employees.csv")


def analyze_csv(file_path=CSV_FILE):
    """Read employee rows and print record, data-quality, and salary summaries."""
    try:
        with file_path.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames:
                print("The CSV file is empty or has no header row.")
                return
            rows = list(reader)
    except FileNotFoundError:
        print(f"CSV file not found: {file_path}")
        return
    except OSError as error:
        print(f"Could not read the CSV file: {error}")
        return

    missing_values = sum(
        1
        for row in rows
        for field in reader.fieldnames
        if not (row.get(field) or "").strip()
    )
    duplicate_count = len(rows) - len({tuple(row.get(field, "") for field in reader.fieldnames) for row in rows})
    salaries = []
    department_counts = Counter()
    department_salaries = defaultdict(list)
    invalid_salary_count = 0

    for row in rows:
        department = (row.get("Department") or "").strip()
        if department:
            department_counts[department] += 1
        salary_text = (row.get("Salary") or "").strip()
        if salary_text:
            try:
                salary = float(salary_text)
            except ValueError:
                invalid_salary_count += 1
                continue
            salaries.append(salary)
            if department:
                department_salaries[department].append(salary)

    print(f"Total record count: {len(rows)}")
    print(f"Missing values: {missing_values}")
    print(f"Duplicate records: {duplicate_count}")
    if salaries:
        print(f"Average salary: {sum(salaries) / len(salaries):.2f}")
        print(f"Minimum salary: {min(salaries):.2f}")
        print(f"Maximum salary: {max(salaries):.2f}")
    else:
        print("Salary statistics: unavailable (no valid salary values).")
    if invalid_salary_count:
        print(f"Invalid salary values skipped: {invalid_salary_count}")

    print("Department-wise employee count:")
    if department_counts:
        for department, count in sorted(department_counts.items()):
            print(f"  {department}: {count}")
    else:
        print("  No department values.")

    print("Department-wise average salary:")
    if department_salaries:
        for department, values in sorted(department_salaries.items()):
            print(f"  {department}: {sum(values) / len(values):.2f}")
    else:
        print("  No valid department salary values.")


if __name__ == "__main__":
    analyze_csv()