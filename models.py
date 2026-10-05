
from __future__ import annotations

from dataclasses import dataclass, field



def validate_email(email: str) -> str:
    
    email = email.strip()
    local, at, domain = email.partition("@")
    if not local or not at:
        raise ValueError("Email must contain '@' with text before it.")
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise ValueError("Email needs a domain like example.com.")
    return email


def validate_age(text: str) -> int:
    
    try:
        age = int(text)
    except ValueError:
        raise ValueError("Age must be a whole number.") from None
    if not 5 <= age <= 25:
        raise ValueError("Age must be between 5 and 25.")
    return age


def validate_grade(text: str) -> int:
    
    try:
        grade = int(text)
    except ValueError:
        raise ValueError("Grade must be a whole number.") from None
    if not 0 <= grade <= 100:
        raise ValueError("Grade must be between 0 and 100.")
    return grade


def validate_name(name: str) -> str:
   
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    return name


@dataclass
class Student:
   

    id: int
    name: str
    email: str
    age: int
    grades: dict[str, int] = field(default_factory=dict)

    def average(self) -> float | None:
        
        if not self.grades:
            return None
        return sum(self.grades.values()) / len(self.grades)

    def to_dict(self) -> dict:
        
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "grades": self.grades,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """Build a Student from a dict loaded from JSON."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            age=data["age"],
            grades=data.get("grades", {}),
        )