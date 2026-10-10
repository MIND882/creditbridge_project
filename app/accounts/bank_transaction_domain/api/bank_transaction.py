"""

HTTP surface for Bank Transaction.



Submittable, so it adds ``/submit``, ``/cancel`` and ``/discard``. ``/discard``

is the ``on_discard`` hook: it drops an unreconciled transaction without going

through the submit/cancel pair.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_transaction_domain.models.bank_transaction import BankTransactionStatus

from app.accounts.bank_transaction_domain.schemas.bank_transaction import (

    BankTransactionCreate,

    BankTransactionListResponse,

    BankTransactionRead,

    BankTransactionStatusResult,

    BankTransactionUpdate,

)

from app.accounts.bank_transaction_domain.services.bank_transaction_service import (

    BankTransactionService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankTransactionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankTransactionRead:

    return BankTransactionRead.model_validate(row)





def _status(row: object) -> BankTransactionStatusResult:

    return BankTransactionStatusResult(

        id=row.id,  # type: ignore[attr-defined]

        name=row.name,  # type: ignore[attr-defined]

        docstatus=int(row.docstatus),  # type: ignore[attr-defined]

        status=row.status,  # type: ignore[attr-defined]

        allocated_amount=row.allocated_amount,  # type: ignore[attr-defined]

        unallocated_amount=row.unallocated_amount,  # type: ignore[attr-defined]

    )





@router.post(

    "",

    response_model=BankTransactionRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a bank transaction (draft)",

)

def create_bank_transaction(

    payload: BankTransactionCreate, db: DbDep, business_id: BusinessDep

) -> BankTransactionRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankTransactionListResponse, summary="List bank transactions")

def list_bank_transactions(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    status_filter: Optional[BankTransactionStatus] = Query(default=None, alias="status"),

    bank_account_id: Optional[uuid.UUID] = Query(default=None),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

    docstatus: Optional[int] = Query(default=None, ge=0, le=2),

    include_cancelled: bool = Query(default=False),

) -> BankTransactionListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        status=status_filter,

        bank_account_id=bank_account_id,

        from_date=from_date,

        to_date=to_date,

        search=search,

        docstatus=docstatus,

        include_cancelled=include_cancelled,

    )

    return BankTransactionListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{transaction_id}", response_model=BankTransactionRead, summary="Get one transaction"

)

def get_bank_transaction(

    transaction_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankTransactionRead:

    try:

        return _read(_service.get(db, business_id, transaction_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{transaction_id}", response_model=BankTransactionRead, summary="Update a transaction"

)

def update_bank_transaction(

    transaction_id: uuid.UUID,

    payload: BankTransactionUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> BankTransactionRead:

    try:

        return _read(_service.update(db, business_id, transaction_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{transaction_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a draft transaction",

)

def delete_bank_transaction(

    transaction_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, transaction_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{transaction_id}/submit",

    response_model=BankTransactionStatusResult,

    summary="Submit (draft -> submitted)",

)

def submit_bank_transaction(

    transaction_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankTransactionStatusResult:

    try:

        return _status(_service.submit(db, business_id, transaction_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{transaction_id}/cancel",

    response_model=BankTransactionStatusResult,

    summary="Cancel (submitted -> cancelled)",

)

def cancel_bank_transaction(

    transaction_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankTransactionStatusResult:

    try:

        return _status(_service.cancel(db, business_id, transaction_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/{transaction_id}/discard",

    response_model=BankTransactionStatusResult,

    summary="Discard an unreconciled transaction",

)

def discard_bank_transaction(

    transaction_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankTransactionStatusResult:

    try:

        return _status(_service.discard(db, business_id, transaction_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
