import logging
from datetime import datetime
from typing import Any

import pronotepy
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google.cloud import firestore
from jsondiff import diff

from app.api.deps import get_db, get_pronote
from app.core import config
from app.utils.schedule import Schedule, WeekSchedule

log = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Set templates filters.
def rank(lesson: dict) -> dict:
    """Returns the rank of the lesson in the schedule."""
    start = datetime.strptime(lesson["start"], "%H:%M")
    end = datetime.strptime(lesson["end"], "%H:%M")

    rank_start = (start - datetime.strptime(config.day_start, "%H:%M")).seconds // 60 // config.lesson_duration
    rank_end = (end - datetime.strptime(config.day_start, "%H:%M")).seconds // 60 // config.lesson_duration

    return {
        "start": rank_start,
        "end": rank_end,
        "duration": rank_end - rank_start,
    }


templates.env.filters["rank"] = rank


@router.put("", status_code=status.HTTP_200_OK, response_class=Response)
def refresh_schedules(
        date_from: str, date_to: str,
        db: firestore.Client = Depends(get_db), pronote: pronotepy.Client = Depends(get_pronote)
) -> Any:
    """Refresh the schedule from Pronote. The dates should be in the format of YYYY-MM-DD."""
    user_ref = db.collection("users").document(pronote.username)
    schedule_ref = user_ref.collection("schedule")

    # Get the schedule from Pronote starting from `date_from` and ending at `date_to`.
    # We should first convert the dates to datetime objects.
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    # Get the schedule from Pronote.
    schedule = Schedule(
        schedule_ref.where("date", ">=", date_from).where("date", "<=", date_to).get(),
        pronote.lessons(date_from, date_to),
    )

    for date, lessons in schedule:
        if not lessons["existing"]:
            # If there is no document, create one.
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            schedule_ref.add({
                "date": date_obj,
                "week": int((date_obj - relativedelta(weeks=34)).strftime("%U")),
                "lessons": lessons["fetched"]["json"],
            })
            log.info(f"Added schedule for {date}")
        else:
            # Compare the fetched lessons with the existing lessons.
            lessons_diff = diff(lessons["fetched"]["json"], lessons["existing"]["json"])
            lessons_doc: firestore.DocumentSnapshot = lessons["existing"]["doc"]

            # Check if there are any changes.
            if lessons_diff:
                lessons_doc.reference.update({
                    "lessons": lessons["fetched"]["json"],
                })

                log.info(f"Schedule for {date} has been updated, diff: {lessons_diff}")

                # # Add the changes to the pending collection.
                # add_to_pending(db, lessons["fetched"]["json"], lessons_diff, doc=lessons_doc)
                # log.info(f"Pending changes for {date} have been added")
            else:
                log.debug(f"Schedule for {date} is up to date")


@router.get("", response_class=HTMLResponse)
def get_schedules(
        request: Request, week: int = 0, year: int = 0,
        db: firestore.Client = Depends(get_db), pronote: pronotepy.Client = Depends(get_pronote)
) -> Any:
    """Get the schedule in HTML format."""
    user_ref = db.collection("users").document(pronote.username)
    schedule_ref = user_ref.collection("schedule")

    today = datetime.today()
    if not week:
        # Get the current week.
        week = int((today - relativedelta(weeks=34)).strftime("%U"))

    if not year:
        year = today.year

    # Get the week's schedule from the database.
    a = [day.to_dict() for day in schedule_ref.where("week", "==", week).get()]
    schedule = WeekSchedule(week, year, a)

    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "schedule": [(date, lessons) for date, lessons in schedule],
        "diff": {}
    })
