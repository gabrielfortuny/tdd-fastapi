import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from tortoise import connections

from app.config import Settings, get_settings

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    try:
        db = connections.get("default")
        await db.execute_query("SELECT 1")
        db_status = "ok"
    except Exception as e:
        log.error("DB healthcheck failed: %s", e)
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
