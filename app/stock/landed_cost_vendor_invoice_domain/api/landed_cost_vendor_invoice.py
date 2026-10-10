"""HTTP surface for Landed Cost Vendor Invoice -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.landed_cost_vendor_invoice_domain.schemas.landed_cost_vendor_invoice import (

    LandedCostVendorInvoiceListResponse,

    LandedCostVendorInvoiceRead,

)

from app.stock.landed_cost_vendor_invoice_domain.services.landed_cost_vendor_invoice_service import LandedCostVendorInvoiceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LandedCostVendorInvoiceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LandedCostVendorInvoiceListResponse, summary="List landed cost vendor invoice rows")

def list_landed_cost_vendor_invoice(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LandedCostVendorInvoiceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LandedCostVendorInvoiceListResponse.from_result(

        page, [LandedCostVendorInvoiceRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=LandedCostVendorInvoiceRead, summary="Get one landed cost vendor invoice row"

)

def get_landed_cost_vendor_invoice(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LandedCostVendorInvoiceRead:

    try:

        return LandedCostVendorInvoiceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
