"""HTTP surface for Payment Entry. Submittable: /submit and /cancel."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.payment_entry_domain.models.payment_entry import PaymentType

from app.accounts.payment_entry_domain.schemas.payment_entry import (

    PaymentEntryCreate,

    PaymentEntryListResponse,

    PaymentEntryRead,

    PaymentEntryStatusResult,

    PaymentEntryUpdate,

)

from app.accounts.payment_entry_domain.services.payment_entry_service import PaymentEntryService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentEntryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> PaymentEntryRead:

    return PaymentEntryRead.model_validate(row)





def _status(row: object) -> PaymentEntryStatusResult:

    return PaymentEntryStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

        status=row.status,  # type: ignore[attr-defined]

        difference_amount=row.difference_amount,  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=PaymentEntryRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a payment entry (draft)",

)

def create_payment_entry(

    payload: PaymentEntryCreate, db: DbDep, business_id: BusinessDep

) -> PaymentEntryRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PaymentEntryListResponse, summary="List payment entries")

def list_payment_entries(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    payment_type: Optional[PaymentType] = Query(default=None),

    party_type: Optional[str] = Query(default=None, max_length=140),

    party: Optional[str] = Query(default=None, max_length=140),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

) -> PaymentEntryListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        payment_type=payment_type.value if payment_type else None,

        party_type=party_type,

        party=party,

        from_date=from_date,

        to_date=to_date,

        search=search,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

    )

    return PaymentEntryListResponse.from_result(page, [_read(r) for r in page.items])






def _resolve_payment_entry_uuid(
    entry_id: str, db: Session, business_id: uuid.UUID
) -> Optional[uuid.UUID]:
    try:
        return uuid.UUID(entry_id)
    except ValueError:
        e = _service.repository.get_by_name(db, business_id, entry_id)
        return e.id if e else None


@router.get("/{entry_id}", response_model=PaymentEntryRead, summary="Get one payment entry")

def get_payment_entry(entry_id: str, db: DbDep, business_id: BusinessDep) -> PaymentEntryRead:

    try:

        uid = _resolve_payment_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment Entry '{entry_id}' not found")
        return _read(_service.get(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{entry_id}", response_model=PaymentEntryRead, summary="Update a draft entry")

def update_payment_entry(

    entry_id: str, payload: PaymentEntryUpdate, db: DbDep, business_id: BusinessDep

) -> PaymentEntryRead:

    try:

        uid = _resolve_payment_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment Entry '{entry_id}' not found")
        return _read(_service.update(db, business_id, uid, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a draft entry"

)

def delete_payment_entry(entry_id: str, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        uid = _resolve_payment_entry_uuid(entry_id, db, business_id)
        if not uid:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        _service.delete(db, business_id, uid)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{entry_id}/submit",

    response_model=PaymentEntryStatusResult,

    summary="Submit (draft -> submitted) and post the GL entries",

)

def submit_payment_entry(

    entry_id: str, db: DbDep, business_id: BusinessDep

) -> PaymentEntryStatusResult:

    try:

        uid = _resolve_payment_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment Entry '{entry_id}' not found")
        return _status(_service.submit(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{entry_id}/cancel",

    response_model=PaymentEntryStatusResult,

    summary="Cancel (submitted -> cancelled) and reverse the GL entries",

)

def cancel_payment_entry(

    entry_id: str, db: DbDep, business_id: BusinessDep

) -> PaymentEntryStatusResult:

    try:

        uid = _resolve_payment_entry_uuid(entry_id, db, business_id)
        if not uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Payment Entry '{entry_id}' not found")
        return _status(_service.cancel(db, business_id, uid))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
