"""HTTP surface for Sales Invoice Payment -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_payment_domain.schemas.sales_invoice_payment import (

    SalesInvoicePaymentListResponse,

    SalesInvoicePaymentRead,

)

from app.accounts.sales_invoice_payment_domain.services.sales_invoice_payment_service import SalesInvoicePaymentService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SalesInvoicePaymentService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SalesInvoicePaymentListResponse, summary="List sales invoice payment rows")

def list_sales_invoice_payment(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SalesInvoicePaymentListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SalesInvoicePaymentListResponse.from_result(

        page, [SalesInvoicePaymentRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=SalesInvoicePaymentRead, summary="Get one sales invoice payment row")

def get_sales_invoice_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SalesInvoicePaymentRead:

    try:

        return SalesInvoicePaymentRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
