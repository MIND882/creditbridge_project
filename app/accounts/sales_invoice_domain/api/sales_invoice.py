"""HTTP surface for Sales Invoice."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_domain.schemas.sales_invoice import (

        SalesInvoiceCreate,

    SalesInvoiceUpdate,

    SalesInvoiceRead,

    SalesInvoiceListResponse,

)

from app.accounts.sales_invoice_domain.services.sales_invoice_service import SalesInvoiceService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SalesInvoiceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=SalesInvoiceRead, status_code=status.HTTP_201_CREATED,

    summary="Create a sales invoice",

)

def create_sales_invoice(

    payload: SalesInvoiceCreate, db: DbDep, business_id: BusinessDep

) -> SalesInvoiceRead:

    try:

        return SalesInvoiceRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=SalesInvoiceListResponse, summary="List sales invoices")

def list_sales_invoice(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> SalesInvoiceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return SalesInvoiceListResponse.from_result(

        page, [SalesInvoiceRead.model_validate(r) for r in page.items]

    )






def _resolve_sales_invoice_uuid(
    row_id: str, db: Session, business_id: uuid.UUID
) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(row_id)
    except ValueError:
        inv = _service.repository.get_by_name(db, business_id, row_id)
        return inv.id if inv else None

@router.get(

    "/{row_id}", response_model=SalesInvoiceRead, summary="Get one sales invoice"

)

def get_sales_invoice(
    row_id: str, db: DbDep, business_id: BusinessDep
) -> SalesInvoiceRead:
    uid = _resolve_sales_invoice_uuid(row_id, db, business_id)
    if not uid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales Invoice '{row_id}' not found")
    try:
        return SalesInvoiceRead.model_validate(_service.get(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=SalesInvoiceRead, summary="Update")

def update_sales_invoice(
    row_id: str, payload: SalesInvoiceUpdate, db: DbDep, business_id: BusinessDep
) -> SalesInvoiceRead:
    uid = _resolve_sales_invoice_uuid(row_id, db, business_id)
    if not uid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales Invoice '{row_id}' not found")
    try:
        return SalesInvoiceRead.model_validate(_service.update(db, business_id, uid, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_sales_invoice(
    row_id: str, db: DbDep, business_id: BusinessDep
) -> Response:
    uid = _resolve_sales_invoice_uuid(row_id, db, business_id)
    if not uid:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    try:
        _service.delete(db, business_id, uid)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post("/{row_id}/submit", response_model=SalesInvoiceRead, summary="Submit")

def submit_sales_invoice(
    row_id: str, db: DbDep, business_id: BusinessDep
) -> SalesInvoiceRead:
    uid = _resolve_sales_invoice_uuid(row_id, db, business_id)
    if not uid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales Invoice '{row_id}' not found")
    try:
        return SalesInvoiceRead.model_validate(_service.submit(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=SalesInvoiceRead, summary="Cancel")

def cancel_sales_invoice(
    row_id: str, db: DbDep, business_id: BusinessDep
) -> SalesInvoiceRead:
    uid = _resolve_sales_invoice_uuid(row_id, db, business_id)
    if not uid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales Invoice '{row_id}' not found")
    try:
        return SalesInvoiceRead.model_validate(_service.cancel(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
