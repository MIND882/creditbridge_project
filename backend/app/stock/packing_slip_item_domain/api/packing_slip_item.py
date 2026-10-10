"""HTTP surface for Packing Slip Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.packing_slip_item_domain.schemas.packing_slip_item import (

    PackingSlipItemListResponse,

    PackingSlipItemRead,

)

from app.stock.packing_slip_item_domain.services.packing_slip_item_service import PackingSlipItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PackingSlipItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PackingSlipItemListResponse, summary="List packing slip item rows")

def list_packing_slip_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PackingSlipItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PackingSlipItemListResponse.from_result(

        page, [PackingSlipItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=PackingSlipItemRead, summary="Get one packing slip item row"

)

def get_packing_slip_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PackingSlipItemRead:

    try:

        return PackingSlipItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
