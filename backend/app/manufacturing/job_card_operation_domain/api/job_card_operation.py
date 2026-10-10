"""HTTP surface for Job Card Operation -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.job_card_operation_domain.schemas.job_card_operation import (

    JobCardOperationListResponse,

    JobCardOperationRead,

)

from app.manufacturing.job_card_operation_domain.services.job_card_operation_service import JobCardOperationService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = JobCardOperationService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=JobCardOperationListResponse, summary="List job card operation rows")

def list_job_card_operation(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> JobCardOperationListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return JobCardOperationListResponse.from_result(

        page, [JobCardOperationRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=JobCardOperationRead, summary="Get one job card operation row"

)

def get_job_card_operation(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> JobCardOperationRead:

    try:

        return JobCardOperationRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
