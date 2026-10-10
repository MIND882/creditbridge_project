"""HTTP surface for Discounted Invoice -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.discounted_invoice_domain.schemas.discounted_invoice import (

    DiscountedInvoiceListResponse,

    DiscountedInvoiceRead,

)

from app.accounts.discounted_invoice_domain.services.discounted_invoice_service import DiscountedInvoiceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = DiscountedInvoiceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=DiscountedInvoiceListResponse, summary="List discounted invoice rows")

def list_discounted_invoice(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> DiscountedInvoiceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return DiscountedInvoiceListResponse.from_result(

        page, [DiscountedInvoiceRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=DiscountedInvoiceRead, summary="Get one discounted invoice row")

def get_discounted_invoice(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DiscountedInvoiceRead:

    try:

        return DiscountedInvoiceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
