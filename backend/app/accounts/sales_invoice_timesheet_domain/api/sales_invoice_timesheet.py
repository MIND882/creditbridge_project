"""HTTP surface for Sales Invoice Timesheet -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_timesheet_domain.schemas.sales_invoice_timesheet import (

    SalesInvoiceTimesheetListResponse,

    SalesInvoiceTimesheetRead,

)

from app.accounts.sales_invoice_timesheet_domain.services.sales_invoice_timesheet_service import SalesInvoiceTimesheetService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SalesInvoiceTimesheetService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=SalesInvoiceTimesheetListResponse, summary="List sales invoice timesheet rows")

def list_sales_invoice_timesheet(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> SalesInvoiceTimesheetListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return SalesInvoiceTimesheetListResponse.from_result(

        page, [SalesInvoiceTimesheetRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=SalesInvoiceTimesheetRead, summary="Get one sales invoice timesheet row")

def get_sales_invoice_timesheet(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SalesInvoiceTimesheetRead:

    try:

        return SalesInvoiceTimesheetRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
