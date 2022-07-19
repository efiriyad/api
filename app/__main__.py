import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core import settings

app = FastAPI(title=settings.api.name)

# Mount the static files directory and the routers.
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router, prefix=settings.api.endpoint)

if __name__ == "__main__":
    uvicorn.run("app.__main__:app", host=settings.api.host, port=settings.api.port)
