from fastapi import APIRouter

from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import TextSummary

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()

    return SummaryResponseSchema(id=summary.id, url=payload.url)  # pyright: ignore[reportAttributeAccessIssue]
