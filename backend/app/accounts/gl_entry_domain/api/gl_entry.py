"""

HTTP surface for GL Entry.



Append-only, so there is no PATCH and no DELETE: a correction is a reversal

posted as a new entry, and a reversal is ``/cancel`` plus a fresh set. Adds

``/post`` for a balanced voucher set and ``/balance`` reads.

"""



from __future__ import annotations



import uuid

from datetime import date

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from pydantic import Field

from sqlalchemy.orm import Session



from app.accounts.gl_entry_domain.schemas.gl_entry import (

    AccountBalanceRead,

    GLEntryCreate,

    GLEntryListResponse,

    GLEntryRead,

    GLEntryStatusResult,

)

from app.accounts.gl_entry_domain.services.gl_entry_service import GLEntryService

from app.core.base_schema import InputSchema

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = GLEntryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





class GLEntrySetCreate(InputSchema):

    """A balanced voucher: every row must share the voucher it names."""



    voucher_type: Annotated[str, Field(min_length=1, max_length=140)]

    voucher_no: Annotated[str, Field(min_length=1, max_length=140)]

    entries: Annotated[list[GLEntryCreate], Field(min_length=1)]





def _read(row: object) -> GLEntryRead:

    return GLEntryRead.model_validate(row)





@router.post(

    "", response_model=GLEntryRead, status_code=status.HTTP_201_CREATED,

    summary="Post one GL entry",

)

def create_gl_entry(

    payload: GLEntryCreate, db: DbDep, business_id: BusinessDep

) -> GLEntryRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post(

    "/post",

    response_model=list[GLEntryRead],

    status_code=status.HTTP_201_CREATED,

    summary="Post a balanced voucher set atomically",

)

def post_gl_entry_set(

    payload: GLEntrySetCreate, db: DbDep, business_id: BusinessDep

) -> list[GLEntryRead]:

    try:

        rows = _service.post_balanced_set(

            db,

            business_id,

            payload.entries,

            voucher_type=payload.voucher_type,

            voucher_no=payload.voucher_no,

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return [_read(r) for r in rows]





@router.get("", response_model=GLEntryListResponse, summary="List GL entries")

def list_gl_entries(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    account_id: Optional[uuid.UUID] = Query(default=None),

    cost_center_id: Optional[uuid.UUID] = Query(default=None),

    voucher_type: Optional[str] = Query(default=None, max_length=140),

    voucher_no: Optional[str] = Query(default=None, max_length=140),

    party_type: Optional[str] = Query(default=None, max_length=140),

    party: Optional[str] = Query(default=None, max_length=140),

    from_date: Optional[date] = Query(default=None),

    to_date: Optional[date] = Query(default=None),

    include_cancelled: bool = Query(default=False),

) -> GLEntryListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        account_id=account_id,

        cost_center_id=cost_center_id,

        voucher_type=voucher_type,

        voucher_no=voucher_no,

        party_type=party_type,

        party=party,

        from_date=from_date,

        to_date=to_date,

        include_cancelled=include_cancelled,

    )

    return GLEntryListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/balance/{account_id}",

    response_model=AccountBalanceRead,

    summary="Debit-credit balance for one account",

)

def get_account_balance(

    account_id: uuid.UUID,

    db: DbDep,

    business_id: BusinessDep,

    include_cancelled: bool = Query(default=False),

) -> AccountBalanceRead:

    debit, credit = _service.repository.account_balance(

        db, business_id, account_id, include_cancelled=include_cancelled

    )

    return AccountBalanceRead(

        account_id=account_id,

        balance=debit - credit,

        total_debit=debit,

        total_credit=credit,

    )





@router.get(

    "/{entry_id}", response_model=GLEntryRead, summary="Get one GL entry"

)

def get_gl_entry(entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> GLEntryRead:

    try:

        return _read(_service.get(db, business_id, entry_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.post(

    "/{entry_id}/cancel",

    response_model=GLEntryStatusResult,

    summary="Cancel a GL entry",

)

def cancel_gl_entry(

    entry_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> GLEntryStatusResult:

    try:

        row = _service.cancel(db, business_id, entry_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc



    return GLEntryStatusResult(

        id=row.id, name=row.name, docstatus=row.docstatus, is_cancelled=row.is_cancelled

    )
