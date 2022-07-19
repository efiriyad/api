import datetime

from pydantic import BaseModel


class Lesson(BaseModel):
    """The schedule lesson model."""

    background_color: str
    classrooms: list[str]
    end: datetime.time
    group_names: list[str]
    start: datetime.time
    status: str
    subject: str
    teachers: list[str]


class Schedule(BaseModel):
    """The schedule model."""

    date: datetime.datetime
    lessons: list[Lesson]
