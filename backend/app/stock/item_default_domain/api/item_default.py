"""HTTP surface for Item Default -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.item_default_domain.schemas.item_default import (

    ItemDefaultListResponse,

    ItemDefaultRead,

)

from app.stock.item_default_domain.services.item_default_service import ItemDefaultService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemDefaultService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemDefaultListResponse, summary="List item default rows")

def list_item_default(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ItemDefaultListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ItemDefaultListResponse.from_result(

        page, [ItemDefaultRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemDefaultRead, summary="Get one item default row"

)

def get_item_default(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemDefaultRead:

    try:

        return ItemDefaultRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
