"""HTTP surface for Purchase Order Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.buying.purchase_order_item_domain.schemas.purchase_order_item import (

    PurchaseOrderItemListResponse,

    PurchaseOrderItemRead,

)

from app.buying.purchase_order_item_domain.services.purchase_order_item_service import PurchaseOrderItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PurchaseOrderItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PurchaseOrderItemListResponse, summary="List purchase order item rows")

def list_purchase_order_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PurchaseOrderItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PurchaseOrderItemListResponse.from_result(

        page, [PurchaseOrderItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=PurchaseOrderItemRead, summary="Get one purchase order item row"

)

def get_purchase_order_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PurchaseOrderItemRead:

    try:

        return PurchaseOrderItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
