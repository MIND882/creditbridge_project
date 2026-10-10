"""HTTP surface for Item Customer Detail -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.item_customer_detail_domain.schemas.item_customer_detail import (

    ItemCustomerDetailListResponse,

    ItemCustomerDetailRead,

)

from app.stock.item_customer_detail_domain.services.item_customer_detail_service import ItemCustomerDetailService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemCustomerDetailService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ItemCustomerDetailListResponse, summary="List item customer detail rows")

def list_item_customer_detail(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ItemCustomerDetailListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ItemCustomerDetailListResponse.from_result(

        page, [ItemCustomerDetailRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ItemCustomerDetailRead, summary="Get one item customer detail row"

)

def get_item_customer_detail(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemCustomerDetailRead:

    try:

        return ItemCustomerDetailRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
