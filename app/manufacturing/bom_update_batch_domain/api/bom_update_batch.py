"""HTTP surface for BOM Update Batch -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.bom_update_batch_domain.schemas.bom_update_batch import (

    BomUpdateBatchListResponse,

    BomUpdateBatchRead,

)

from app.manufacturing.bom_update_batch_domain.services.bom_update_batch_service import BomUpdateBatchService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BomUpdateBatchService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=BomUpdateBatchListResponse, summary="List bom update batch rows")

def list_bom_update_batch(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BomUpdateBatchListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return BomUpdateBatchListResponse.from_result(

        page, [BomUpdateBatchRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=BomUpdateBatchRead, summary="Get one bom update batch row"

)

def get_bom_update_batch(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BomUpdateBatchRead:

    try:

        return BomUpdateBatchRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
