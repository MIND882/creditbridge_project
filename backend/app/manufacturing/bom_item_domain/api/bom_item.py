"""HTTP surface for BOM Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.bom_item_domain.schemas.bom_item import (

    BomItemListResponse,

    BomItemRead,

)

from app.manufacturing.bom_item_domain.services.bom_item_service import BomItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BomItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=BomItemListResponse, summary="List bom item rows")

def list_bom_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BomItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return BomItemListResponse.from_result(

        page, [BomItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=BomItemRead, summary="Get one bom item row"

)

def get_bom_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BomItemRead:

    try:

        return BomItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
