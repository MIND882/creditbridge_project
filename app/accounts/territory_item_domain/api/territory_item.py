"""HTTP surface for Territory Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.territory_item_domain.schemas.territory_item import (

    TerritoryItemListResponse,

    TerritoryItemRead,

)

from app.accounts.territory_item_domain.services.territory_item_service import TerritoryItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TerritoryItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=TerritoryItemListResponse, summary="List territory item rows")

def list_territory_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> TerritoryItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return TerritoryItemListResponse.from_result(

        page, [TerritoryItemRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=TerritoryItemRead, summary="Get one territory item row")

def get_territory_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> TerritoryItemRead:

    try:

        return TerritoryItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
