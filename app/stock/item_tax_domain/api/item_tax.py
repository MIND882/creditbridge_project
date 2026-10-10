"""HTTP surface for Item Tax -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.item_tax_domain.schemas.item_tax import (

    ItemTaxListResponse,

    ItemTaxRead,

)

from app.stock.item_tax_domain.services.item_tax_service import ItemTaxService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemTaxService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemTaxListResponse, summary="List item tax rows")

def list_item_tax(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ItemTaxListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ItemTaxListResponse.from_result(

        page, [ItemTaxRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemTaxRead, summary="Get one item tax row"

)

def get_item_tax(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemTaxRead:

    try:

        return ItemTaxRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
