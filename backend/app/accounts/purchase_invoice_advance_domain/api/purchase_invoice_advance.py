"""HTTP surface for Purchase Invoice Advance -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.purchase_invoice_advance_domain.schemas.purchase_invoice_advance import (

    PurchaseInvoiceAdvanceListResponse,

    PurchaseInvoiceAdvanceRead,

)

from app.accounts.purchase_invoice_advance_domain.services.purchase_invoice_advance_service import PurchaseInvoiceAdvanceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PurchaseInvoiceAdvanceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PurchaseInvoiceAdvanceListResponse, summary="List purchase invoice advance rows")

def list_purchase_invoice_advance(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PurchaseInvoiceAdvanceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PurchaseInvoiceAdvanceListResponse.from_result(

        page, [PurchaseInvoiceAdvanceRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PurchaseInvoiceAdvanceRead, summary="Get one purchase invoice advance row")

def get_purchase_invoice_advance(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PurchaseInvoiceAdvanceRead:

    try:

        return PurchaseInvoiceAdvanceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
