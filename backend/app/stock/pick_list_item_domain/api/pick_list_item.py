"""HTTP surface for Pick List Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.pick_list_item_domain.schemas.pick_list_item import (

    PickListItemListResponse,

    PickListItemRead,

)

from app.stock.pick_list_item_domain.services.pick_list_item_service import PickListItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PickListItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PickListItemListResponse, summary="List pick list item rows")

def list_pick_list_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PickListItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PickListItemListResponse.from_result(

        page, [PickListItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=PickListItemRead, summary="Get one pick list item row"

)

def get_pick_list_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PickListItemRead:

    try:

        return PickListItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
