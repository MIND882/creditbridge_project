"""HTTP surface for Quality Inspection Reading -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.quality_inspection_reading_domain.schemas.quality_inspection_reading import (

    QualityInspectionReadingListResponse,

    QualityInspectionReadingRead,

)

from app.stock.quality_inspection_reading_domain.services.quality_inspection_reading_service import QualityInspectionReadingService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = QualityInspectionReadingService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=QualityInspectionReadingListResponse, summary="List quality inspection reading rows")

def list_quality_inspection_reading(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> QualityInspectionReadingListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return QualityInspectionReadingListResponse.from_result(

        page, [QualityInspectionReadingRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=QualityInspectionReadingRead, summary="Get one quality inspection reading row"

)

def get_quality_inspection_reading(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> QualityInspectionReadingRead:

    try:

        return QualityInspectionReadingRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
