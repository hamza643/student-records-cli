
from __future__ import annotations

from typing import Callable, TypeVar

from models import (
    Student,
    validate_age,
    validate_email,
    validate_grade,
    validate_name,
)
from stats import build_report
from storage import load_data, save_data, save_report

T = TypeVar("T")


def ask(prompt: str, validator: Callable[[str], T]) -> T:
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as error:
            print(f"  x {error} Try again.")


def validate_id(text: str) -> int:
    """Convert text to a whole-number id."""
    try:
        return int(text)
    except ValueError:
        raise ValueError("Id must be a whole number.") from None


def find_by_id(students: list[Student], student_id: int) -> Student | None:
    """Return the student with this id, or None."""
    return next((s for s in students if s.id == student_id), None)


def search_students(students: list[Student], query: str) -> list[Student]:
    """Return students whose name contains the query, or whose email matches exactly."""
    query = query.strip().lower()
    return [s for s in students if query in s.name.lower() or query == s.email.lower()]


def print_table(students: list[Student]) -> None:
    """Print students in an aligned table, sorted by name."""
    print(f"{'ID':>3}  {'Name':<15}  {'Email':<22}  {'Age':>3}  {'Avg':>5}")
    for s in sorted(students, key=lambda s: s.name.lower()):
        avg = s.average()
        avg_text = f"{avg:.1f}" if avg is not None else "-"
        print(f"{s.id:>3}  {s.name:<15}  {s.email:<22}  {s.age:>3}  {avg_text:>5}")


def add_student(students: list[Student], next_id: int) -> tuple[list[Student], int]:
    """Ask for a new student's details and return the updated list and next id."""
    name = ask("Name: ", validate_name)
    email = ask("Email: ", validate_email)
    age = ask("Age: ", validate_age)

    grades: dict[str, int] = {}
    print("Add grades (blank subject to finish)")
    while True:
        subject = input("  Subject: ").strip().lower()
        if not subject:
            break
        grades[subject] = ask("  Grade: ", validate_grade)

    student = Student(next_id, name, email, age, grades)
    print(f"Student added with id {next_id}.")
    return students + [student], next_id + 1


def list_students(students: list[Student]) -> None:
    """Print all students, or a message if there are none."""
    if not students:
        print("No students yet.")
        return
    print_table(students)


def search_menu(students: list[Student]) -> None:
    """Ask for a search term and print the matches."""
    query = input("Search by partial name or exact email: ")
    if not query.strip():
        print("Nothing to search for.")
        return
    matches = search_students(students, query)
    if matches:
        print_table(matches)
    else:
        print("No students found.")


def update_student(students: list[Student]) -> bool:
    """Update one student's email, age, or a grade. Return True if something changed."""
    if not students:
        print("No students yet.")
        return False
    student = find_by_id(students, ask("Student id: ", validate_id))
    if student is None:
        print("No student with that id.")
        return False

    print(f"Updating {student.name}: 1. Email  2. Age  3. A subject grade")
    choice = input("What do you want to change? ").strip()
    if choice == "1":
        student.email = ask("New email: ", validate_email)
    elif choice == "2":
        student.age = ask("New age: ", validate_age)
    elif choice == "3":
        subject = input("Subject: ").strip().lower()
        if not subject:
            print("Subject cannot be empty.")
            return False
        student.grades[subject] = ask("New grade: ", validate_grade)
    else:
        print("Please choose 1, 2 or 3.")
        return False
    print("Student updated.")
    return True


def delete_student(students: list[Student]) -> list[Student]:
    """Delete a student by id after confirmation. Return the new list."""
    if not students:
        print("No students yet.")
        return students
    student = find_by_id(students, ask("Student id: ", validate_id))
    if student is None:
        print("No student with that id.")
        return students
    answer = input(f"Delete {student.name}? (y/n): ").strip().lower()
    if answer != "y":
        print("Cancelled.")
        return students
    print("Student deleted.")
    return [s for s in students if s.id != student.id]


def export_report(students: list[Student]) -> None:
    """Write the statistics report to report.txt."""
    error = save_report(build_report(students))
    print(error if error else "Report saved to report.txt.")


def show_menu() -> None:
    
    print("\n=== Student Records Manager ===")
    print("1. Add student")
    print("2. List all students")
    print("3. Search")
    print("4. Update student")
    print("5. Delete student")
    print("6. Statistics")
    print("7. Export report")
    print("8. Exit")


def save_and_warn(students: list[Student], next_id: int) -> None:
    """Save the data and print an error message if saving failed."""
    error = save_data(students, next_id)
    if error:
        print(error)


def main() -> None:
   
    students, next_id, warning = load_data()
    if warning:
        print(f"Warning: {warning}")

    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            students, next_id = add_student(students, next_id)
            save_and_warn(students, next_id)
        elif choice == "2":
            list_students(students)
        elif choice == "3":
            search_menu(students)
        elif choice == "4":
            if update_student(students):
                save_and_warn(students, next_id)
        elif choice == "5":
            students = delete_student(students)
            save_and_warn(students, next_id)
        elif choice == "6":
            print("\n=== Statistics ===")
            print(build_report(students))
        elif choice == "7":
            export_report(students)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()

    