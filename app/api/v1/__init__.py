from app.api.v1 import schedule, grades
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
