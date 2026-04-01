from typing import List

from fastapi import APIRouter, HTTPException

from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema, TextSummary

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> TextSummary:
    summary = await TextSummary.create(url=payload.url, summary="dummy summary")
    return summary


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:  # type: ignore[valid-type]
    summary = await TextSummary.filter(id=id).first().values()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:  # type: ignore[valid-type]
    summaries = await TextSummary.all().values()
    return summaries
