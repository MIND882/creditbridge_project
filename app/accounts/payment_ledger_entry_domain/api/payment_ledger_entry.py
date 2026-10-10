"""HTTP surface for Payment Ledger Entry. Submittable: /submit and /cancel."""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.payment_ledger_entry_domain.models.payment_ledger_entry import PLEAccountType

from app.accounts.payment_ledger_entry_domain.schemas.payment_ledger_entry import (

    OutstandingRead,

    PaymentLedgerEntryCreate,

    PaymentLedgerEntryListResponse,

    PaymentLedgerEntryRead,

    PaymentLedgerEntryStatusResult,

    PaymentLedgerEntryUpdate,

)

from app.accounts.payment_ledger_entry_domain.services.payment_ledger_entry_service import (

    PaymentLedgerEntryService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentLedgerEntryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> PaymentLedgerEntryRead:

    return PaymentLedgerEntryRead.model_validate(row)





def _status(row: object) -> PaymentLedgerEntryStatusResult:

    return PaymentLedgerEntryStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

        delinked=bool(row.delinked),  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=PaymentLedgerEntryRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a payment ledger entry",

)

def create_payment_ledger_entry(

    payload: PaymentLedgerEntryCreate, db: DbDep, business_id: BusinessDep

) -> PaymentLedgerEntryRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PaymentLedgerEntryListResponse, summary="List ledger entries")

def list_payment_ledger_entries(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    account_id: Optional[uuid.UUID] = Query(default=None),

    account_type: Optional[PLEAccountType] = Query(default=None),

    party_type: Optional[str] = Query(default=None, max_length=140),

    party: Optional[str] = Query(default=None, max_length=140),

    against_voucher_no: Optional[str] = Query(default=None, max_length=140),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

    delinked: Optional[bool] = Query(default=None),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

    search: Optional[str] = Query(default=None, max_length=140),

) -> PaymentLedgerEntryListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        account_id=account_id,

        account_type=account_type.value if account_type else None,

        party_type=party_type,

        party=party,

        against_voucher_no=against_voucher_no,

        from_date=from_date,

        to_date=to_date,

        delinked=delinked,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

        search=search,

    )

    return PaymentLedgerEntryListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/outstanding",

    response_model=OutstandingRead,

    summary="Running balance for a party or a single invoice",

)

def get_outstanding(

    db: DbDep,

    business_id: BusinessDep,

    account_id: Optional[uuid.UUID] = Query(default=None),

    party_type: Optional[str] = Query(default=None, max_length=140),

    party: Optional[str] = Query(default=None, max_length=140),

    against_voucher_no: Optional[str] = Query(default=None, max_length=140),

) -> OutstandingRead:

    """

    Declared before ``/{entry_id}`` so "outstanding" is not swallowed as an id.

    """

    return _service.outstanding(

        db,

        business_id,

        account_id=account_id,

        party_type=party_type,

        party=party,

        against_voucher_no=against_voucher_no,

    )





@router.get("/{entry_id}", response_model=PaymentLedgerEntryRead, summary="Get one entry")

def get_payment_ledger_entry(

    entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentLedgerEntryRead:

    try:

        return _read(_service.get(db, business_id, entry_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{entry_id}", response_model=PaymentLedgerEntryRead, summary="Delink or relink")

def update_payment_ledger_entry(

    entry_id: uuid.UUID, payload: PaymentLedgerEntryUpdate, db: DbDep, business_id: BusinessDep

) -> PaymentLedgerEntryRead:

    try:

        return _read(_service.update(db, business_id, entry_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a draft entry"

)

def delete_payment_ledger_entry(

    entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, entry_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{entry_id}/submit",

    response_model=PaymentLedgerEntryStatusResult,

    summary="Submit (draft -> submitted)",

)

def submit_payment_ledger_entry(

    entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentLedgerEntryStatusResult:

    try:

        return _status(_service.submit(db, business_id, entry_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{entry_id}/cancel",

    response_model=PaymentLedgerEntryStatusResult,

    summary="Cancel (submitted -> cancelled)",

)

def cancel_payment_ledger_entry(

    entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentLedgerEntryStatusResult:

    try:

        return _status(_service.cancel(db, business_id, entry_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
