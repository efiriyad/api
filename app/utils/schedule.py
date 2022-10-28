import logging
from datetime import datetime
from typing import Any, Union

from dateutil.relativedelta import relativedelta
from google.cloud import firestore
from pronotepy.dataClasses import Lesson

from app.core import config

log = logging.getLogger(__name__)


class Schedule:
    """Represents a collection of cached schedules and newly fetched schedules."""

    def __init__(self, existing_lessons: list[firestore.DocumentSnapshot], pronote_lessons: list[Lesson]):
        # Group the lessons by day.
        fetched_lessons_per_day = {}
        for lesson in pronote_lessons:
            day = lesson.start.strftime("%Y-%m-%d")
            if day not in fetched_lessons_per_day:
                fetched_lessons_per_day[day] = []
            fetched_lessons_per_day[day].append(lesson)

        # Jsonify the fetched lessons.
        fetched_lessons_json = {
            day: {
                "json": jsonify_schedule(fetched_lessons),
            } for day, fetched_lessons in fetched_lessons_per_day.items()
        }

        existing_lessons_json = {
            lesson.to_dict()["date"].strftime("%Y-%m-%d"): {
                "json": [dict(sorted(less.items())) for less in lesson.to_dict()["lessons"]],
                "doc": lesson,
            } for lesson in existing_lessons
        }

        # Group both the fetched and existing lessons into a single dictionary.
        self.lessons = {}
        for day, fetched_lessons in sorted(fetched_lessons_json.items()):
            if day not in self.lessons:
                self.lessons[day] = {}

            self.lessons[day]["fetched"] = fetched_lessons
            self.lessons[day]["existing"] = existing_lessons_json[day] if day in existing_lessons_json else []

    def __iter__(self):
        for date, lessons in self.lessons.items():
            yield date, lessons


class WeekSchedule:
    """Represents a collection of a week's schedule."""

    def __init__(self, week: int, year: int, schedule: list[dict]):
        # Sort the schedule by date.
        schedule.sort(key=lambda d: d["date"])

        # Get the week's dates.
        # Revert the week back to normal.
        real_week = week + 33
        date = datetime(year - 1, 1, 3) + relativedelta(weeks=real_week)  # Always start on sunday.

        # Create a list of the week's days
        weekdays = [
            {"date": date + relativedelta(days=i), "lessons": []}
            for i in range(7)
        ]

        # Fill the missing week days with emtpy dictionaries.
        if 1 < len(schedule) < 6:
            # Fill the week days with its corresponding schedule if it exists.
            for day in schedule:
                try:
                    weekday = next(d for d in weekdays if d["date"].date() == day["date"].date())
                    weekday["lessons"] = day["lessons"]
                except StopIteration:
                    log.error(f"{day['date']} was not found in the schedule")
                    break

        # Remove Friday from the weekdays list.
        weekdays.pop(5)

        self.schedule = weekdays

    def __iter__(self):
        for day in self.schedule:
            yield day["date"], day["lessons"]

    def __len__(self):
        return len(self.schedule)


def jsonify_schedule(schedule: list[Lesson]) -> list[dict[str, Any]]:
    """Convert a Pronote schedule to a JSON-friendly format."""
    day_start = datetime.strptime(config.day_start, "%H:%M")
    day_end = datetime.strptime(config.day_end, "%H:%M")
    day_duration = (day_end - day_start).seconds // 60

    # Create a list of slots with a default value of None.
    schedule_slots: list[Union[Lesson, None]] = [None] * (day_duration // config.lesson_duration)

    # Iterate over the schedule and fill the slots.
    # schedule_slots[0] represents the first lesson of the day.
    for lesson in schedule:
        rank_start = (lesson.start - day_start).seconds // 60 // config.lesson_duration
        rank_end = (lesson.end - day_start).seconds // 60 // config.lesson_duration
        for rank in range(rank_start, rank_end):
            # If the slot is already filled, check if the lesson is canceled. If it is, loop over all the slots again
            # and remove the canceled lesson from the slot. Then, add the lesson to the slot.
            if schedule_slots[rank] is not None:
                if schedule_slots[rank].canceled:
                    target_lesson = schedule_slots[rank]
                    for rank_cancel in range(len(schedule_slots)):
                        if schedule_slots[rank_cancel] is target_lesson:
                            schedule_slots[rank_cancel] = None

                    # Now, add the lesson to the slot.
                    schedule_slots[rank] = lesson
                else:
                    if lesson.canceled:
                        for lesson_cancel in range(len(schedule_slots)):
                            if schedule_slots[lesson_cancel] is lesson:
                                schedule_slots[lesson_cancel] = None

            else:
                schedule_slots[rank] = lesson

    # Now, JSONify the schedule. We can ignore the `None` slots.
    schedule_json = []

    for lesson in set(schedule_slots):
        if lesson is not None:
            schedule_json.append({
                "background_color": lesson.background_color,
                "classrooms": lesson.classrooms,
                "end": lesson.end.strftime("%H:%M"),
                "group_names": lesson.group_names,
                "start": lesson.start.strftime("%H:%M"),
                "status": lesson.status,
                "subject": lesson.subject.name,
                "teachers": lesson.teacher_names,
            })

    # Finally, sort the lessons by start time.
    schedule_json.sort(key=lambda l: l["start"])
    return schedule_json


def add_to_pending(
        db: firestore.Client, fetched_lessons: list[dict], diff: dict, doc: firestore.DocumentSnapshot
) -> None:
    """Add a document to the pending collection."""
    pending_ref = db.collection("pending")

    # # Convert the keys of `diff` to strings.
    # diff_str = {str(key): value for key, value in diff.items()}

    pending_ref.document(doc.id).set({
        "type": "schedule",
    })
