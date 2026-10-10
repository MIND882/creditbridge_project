"""HTTP surface for Landed Cost Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.landed_cost_item_domain.schemas.landed_cost_item import (

    LandedCostItemListResponse,

    LandedCostItemRead,

)

from app.stock.landed_cost_item_domain.services.landed_cost_item_service import LandedCostItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LandedCostItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LandedCostItemListResponse, summary="List landed cost item rows")

def list_landed_cost_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LandedCostItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LandedCostItemListResponse.from_result(

        page, [LandedCostItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=LandedCostItemRead, summary="Get one landed cost item row"

)

def get_landed_cost_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LandedCostItemRead:

    try:

        return LandedCostItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
