import logging
from typing import Any

import pronotepy
from fastapi import APIRouter, Depends
from google.cloud import firestore
from jsondiff import diff

from app.api.deps import get_db, get_pronote
from app.core import config
from app.utils.grades import Grades

log = logging.getLogger(__name__)

router = APIRouter()


@router.put("")
def refresh_grades(
        backup: bool = False, periods: list[str] = None,
        db: firestore.Client = Depends(get_db), pronote: pronotepy.Client = Depends(get_pronote)
) -> Any:
    """Refresh the schedule from Pronote. The dates should be in the format of YYYY-MM-DD."""
    user_ref = db.collection("users").document(pronote.username)
    if backup:
        grades_ref = user_ref.collection("backup").document(config.backup_years).collection("grades")
        log.info("Refreshing backup grades")
    else:
        grades_ref = user_ref.collection("grades")
        log.info("Refreshing grades")

    # Get the grades from Pronote.
    pronote_periods = pronote.periods
    if periods:
        pronote_periods = [period for period in pronote_periods if period.name in periods]

    grades = Grades(
        grades_ref.where("period", "in", [p.name for p in periods]).get(),
        [grade for period in pronote_periods for grade in period.grades],
    )

    for grade in grades:
        if not grade["existing"]:
            grades_ref.add(grade["fetched"])
            log.info(f"New grade added ({grade['fetched']['subject']}, {grade['fetched']['date']})")

            # Add the changes to the pending collection.
        else:
            grades_diff = diff(grade["fetched"]["json"], grade["existing"]["json"])
            grade_doc: firestore.DocumentSnapshot = grade["existing"]["doc"]

            # Check if there are any changes.
            if grades_diff:
                grade_doc.reference.update(grade["fetched"]["json"])
                log.info(f"Grade for {grade['fetched']['date']} has been updated, diff: {grades_diff}")

                # Add the changes to the pending collection.
            else:
                log.debug("Grades are up to date")
