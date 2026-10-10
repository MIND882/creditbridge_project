"""HTTP surface for Serial and Batch Entry -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.serial_and_batch_entry_domain.schemas.serial_and_batch_entry import (

    SerialAndBatchEntryListResponse,

    SerialAndBatchEntryRead,

)

from app.stock.serial_and_batch_entry_domain.services.serial_and_batch_entry_service import SerialAndBatchEntryService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SerialAndBatchEntryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SerialAndBatchEntryListResponse, summary="List serial and batch entry rows")

def list_serial_and_batch_entry(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SerialAndBatchEntryListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SerialAndBatchEntryListResponse.from_result(

        page, [SerialAndBatchEntryRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=SerialAndBatchEntryRead, summary="Get one serial and batch entry row"

)

def get_serial_and_batch_entry(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SerialAndBatchEntryRead:

    try:

        return SerialAndBatchEntryRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
