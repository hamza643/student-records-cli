

from __future__ import annotations

from typing import Callable, TypeVar

from models import Student, validate_age, validate_email, validate_grade, validate_name
from storage import load_data, save_data



T = TypeVar("T")


def ask(prompt: str, validator: Callable[[str], T]) -> T:
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as error:
            print(f"  x {error} Try again.")


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
    """Print all students in a table, sorted by name."""
    if not students:
        print("No students yet.")
        return
    print(f"{'ID':>3}  {'Name':<15}  {'Email':<22}  {'Age':>3}  {'Avg':>5}")
    for s in sorted(students, key=lambda s: s.name.lower()):
        avg = s.average()
        avg_text = f"{avg:.1f}" if avg is not None else "-"
        print(f"{s.id:>3}  {s.name:<15}  {s.email:<22}  {s.age:>3}  {avg_text:>5}")


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


def main() -> None:
    """Load data, then run the menu until the user exits."""
    students, next_id, warning = load_data()
    if warning:
        print(f"Warning: {warning}")

    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            students, next_id = add_student(students, next_id)
            error = save_data(students, next_id)
            if error:
                print(error)
        elif choice == "2":
            list_students(students)
        elif choice in {"3", "4", "5", "6", "7"}:
            print("Coming soon.")
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Please, choose a number from 1 to 8.")


if __name__ == "__main__":
    main()