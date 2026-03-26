import logging

from fastapi import FastAPI

from app.api import health
from app.db import init_db

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health.router)

    return application


app = create_application()

init_db(app)
