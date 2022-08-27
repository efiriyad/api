import datetime

from google.cloud import firestore
from pronotepy.dataClasses import Grade


class Grades:
    """Represents a collection of cached grades and newly fetched grades."""

    def __init__(self, existing_grades: list[firestore.DocumentSnapshot], pronote_grades: list[Grade]):
        existing_grades = [{"json": grade.to_dict(), "doc": grade} for grade in existing_grades]
        fetched_grades = jsonify_grades(pronote_grades)

        self.grades = []
        for fetched_grade in sorted(fetched_grades, key=lambda g: g["date"]):
            existing_grade = next(
                filter(lambda g: g["json"]["date"] == fetched_grade["date"], existing_grades),
                {"json": [], "doc": []}
            )

            self.grades.append({
                "fetched": {"json": fetched_grade},
                "existing": {"json": existing_grade["json"], "doc": existing_grade["doc"]},
            })

    def __iter__(self):
        for grade in self.grades:
            return grade


def jsonify_grades(grades: list[Grade]) -> list[dict]:
    """Convert a collection of grades to a JSON-friendly format."""
    return [{
        "average": float(grade.average.replace(",", ".")),
        "coefficient": float(grade.coefficient.replace(",", ".")),
        "comment": grade.comment,
        "date": datetime.date(grade.date.year, grade.date.month, grade.date.day),
        "grade": float(grade.grade.replace(",", ".")),
        "max": float(grade.max.replace(",", ".")),
        "min": float(grade.min.replace(",", ".")),
        "out_of": float(grade.out_of.replace(",", ".")),
        "period": grade.period.name,
        "subject": grade.subject.name,
    } for grade in grades]
