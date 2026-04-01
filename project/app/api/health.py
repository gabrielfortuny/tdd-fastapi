import asyncio
import logging
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from tortoise import connections

from app.config import Settings, get_settings

log = logging.getLogger(__name__)

router = APIRouter()

DB_CHECK_TIMEOUT = 3.0


class StatusEnum(str, Enum):
    ok = "ok"
    degraded = "degraded"
    unavailable = "unavailable"


class HealthResponse(BaseModel):
    status: StatusEnum
    db: StatusEnum
    environment: str
    testing: bool


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_settings)):
    try:
        db = connections.get("default")
        await asyncio.wait_for(db.execute_query("SELECT 1"), timeout=DB_CHECK_TIMEOUT)
        db_status = StatusEnum.ok
    except Exception as e:
        log.error("DB healthcheck failed: %s", e)
        db_status = StatusEnum.unavailable

    response = HealthResponse(
        status=StatusEnum.ok if db_status == StatusEnum.ok else StatusEnum.degraded,
        db=db_status,
        environment=settings.environment,
        testing=settings.testing,
    )

    if db_status != StatusEnum.ok:
        return JSONResponse(content=response.model_dump(), status_code=503)

    return response
