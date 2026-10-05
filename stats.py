
from __future__ import annotations

from datetime import datetime

from models import Student


def class_averages(students: list[Student]) -> dict[str, float]:
   
    grades_by_subject: dict[str, list[int]] = {}
    for student in students:
        for subject, grade in student.grades.items():
            grades_by_subject.setdefault(subject, []).append(grade)
    return {
        subject: sum(grades) / len(grades)
        for subject, grades in sorted(grades_by_subject.items())
    }


def best_and_worst(students: list[Student]) -> tuple[Student | None, Student | None]:
    
    graded = [s for s in students if s.average() is not None]
    if not graded:
        return None, None
    return max(graded, key=Student.average), min(graded, key=Student.average)


def grade_band(average: float) -> str:

    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 55:
        return "C"
    return "F"


def band_counts(students: list[Student]) -> dict[str, int]:

    bands = [grade_band(s.average()) for s in students if s.average() is not None]
    return {letter: bands.count(letter) for letter in "ABCF"}


def build_report(students: list[Student]) -> str:

    highest, lowest = best_and_worst(students)
    lines = [
        f"Report generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"Total students: {len(students)}",
        "Class average by subject:",
    ]
    averages = class_averages(students)
    if averages:
        lines += [f"  {subject:<10} {avg:.1f}" for subject, avg in averages.items()]
    else:
        lines.append("  (no grades yet)")

    if highest and lowest:
        lines.append(f"Highest:  {highest.name} ({highest.average():.1f})")
        lines.append(f"Lowest:   {lowest.name} ({lowest.average():.1f})")
    else:
        lines.append("Highest/Lowest: n/a (no graded students)")

    counts = band_counts(students)
    lines.append("Grade bands:  " + "   ".join(f"{k}: {v}" for k, v in counts.items()))
    return "\n".join(lines)

