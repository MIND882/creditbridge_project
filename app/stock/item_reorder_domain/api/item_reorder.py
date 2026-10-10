"""HTTP surface for Item Reorder -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.item_reorder_domain.schemas.item_reorder import (

    ItemReorderListResponse,

    ItemReorderRead,

)

from app.stock.item_reorder_domain.services.item_reorder_service import ItemReorderService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemReorderService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemReorderListResponse, summary="List item reorder rows")

def list_item_reorder(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ItemReorderListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ItemReorderListResponse.from_result(

        page, [ItemReorderRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemReorderRead, summary="Get one item reorder row"

)

def get_item_reorder(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemReorderRead:

    try:

        return ItemReorderRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
