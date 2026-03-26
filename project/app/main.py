import os

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from tortoise import connections
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings

app = FastAPI()

register_tortoise(
    app,
    db_url=os.environ.get("DATABASE_URL"),
    modules={"models": ["app.models.tortoise"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    try:
        db = connections.get("default")
        await db.execute_query("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    response = {
        "status": "ok" if db_status == "ok" else "degraded",
        "environment": settings.environment,
        "testing": settings.testing,
        "db": db_status,
    }

    if db_status != "ok":
        return JSONResponse(content=response, status_code=503)

    return response
