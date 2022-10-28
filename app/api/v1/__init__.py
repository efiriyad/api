from app.api.v1 import client, grades, schedule
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(client.router, prefix="/client", tags=["client"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
