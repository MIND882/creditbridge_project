"""HTTP surface for Purchase Invoice Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.purchase_invoice_item_domain.schemas.purchase_invoice_item import (

    PurchaseInvoiceItemListResponse,

    PurchaseInvoiceItemRead,

)

from app.accounts.purchase_invoice_item_domain.services.purchase_invoice_item_service import PurchaseInvoiceItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PurchaseInvoiceItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PurchaseInvoiceItemListResponse, summary="List purchase invoice item rows")

def list_purchase_invoice_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PurchaseInvoiceItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PurchaseInvoiceItemListResponse.from_result(

        page, [PurchaseInvoiceItemRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PurchaseInvoiceItemRead, summary="Get one purchase invoice item row")

def get_purchase_invoice_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PurchaseInvoiceItemRead:

    try:

        return PurchaseInvoiceItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
