"""

HTTP surface for Bank Clearance.



Adds the two tool actions as endpoints: ``/get_payment_entries`` (re-fetch the

candidate entries) and ``/update_clearance_date`` (stamp them).

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_clearance_detail_domain.schemas.bank_clearance_detail import (

    BankClearanceDetailRead,

)

from app.accounts.bank_clearance_domain.schemas.bank_clearance import (

    BankClearanceCreate,

    BankClearanceEntriesResult,

    BankClearanceListResponse,

    BankClearanceRead,

    BankClearanceUpdate,

)

from app.accounts.bank_clearance_domain.services.bank_clearance_service import BankClearanceService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankClearanceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankClearanceRead:

    return BankClearanceRead.model_validate(row)





@router.post(

    "",

    response_model=BankClearanceRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a bank clearance run",

)

def create_bank_clearance(

    payload: BankClearanceCreate, db: DbDep, business_id: BusinessDep

) -> BankClearanceRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankClearanceListResponse, summary="List clearance runs")

def list_bank_clearances(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    account_id: Optional[uuid.UUID] = Query(default=None),

) -> BankClearanceListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, account_id=account_id)

    return BankClearanceListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{clearance_id}", response_model=BankClearanceRead, summary="Get one clearance run"

)

def get_bank_clearance(

    clearance_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankClearanceRead:

    try:

        return _read(_service.get(db, business_id, clearance_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{clearance_id}", response_model=BankClearanceRead, summary="Update a clearance run"

)

def update_bank_clearance(

    clearance_id: uuid.UUID,

    payload: BankClearanceUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> BankClearanceRead:

    try:

        return _read(_service.update(db, business_id, clearance_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{clearance_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a clearance run",

)

def delete_bank_clearance(

    clearance_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, clearance_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{clearance_id}/get_payment_entries",

    response_model=BankClearanceEntriesResult,

    summary="Re-fetch the candidate payment entries",

)

def get_payment_entries(

    clearance_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankClearanceEntriesResult:

    try:

        row = _service.get_payment_entries(db, business_id, clearance_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc



    return BankClearanceEntriesResult(

        id=row.id,

        name=row.name,

        refreshed=len(row.payment_entries),

        payment_entries=[BankClearanceDetailRead.model_validate(c) for c in row.payment_entries],

    )





@router.post(

    "/{clearance_id}/update_clearance_date",

    response_model=BankClearanceEntriesResult,

    summary="Apply the clearance dates on the entries",

)

def update_clearance_date(

    clearance_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankClearanceEntriesResult:

    try:

        row, updated = _service.update_clearance_date(db, business_id, clearance_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc



    return BankClearanceEntriesResult(

        id=row.id,

        name=row.name,

        refreshed=updated,

        payment_entries=[BankClearanceDetailRead.model_validate(c) for c in row.payment_entries],

    )
