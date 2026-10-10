"""HTTP surface for Accounting Period (not a tree, not submittable)."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.accounting_period_domain.schemas.accounting_period import (

    AccountingPeriodCreate,

    AccountingPeriodListResponse,

    AccountingPeriodRead,

    AccountingPeriodUpdate,

)

from app.accounts.accounting_period_domain.services.accounting_period_service import (

    AccountingPeriodService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AccountingPeriodService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> AccountingPeriodRead:

    return AccountingPeriodRead.model_validate(row)





@router.post(

    "",

    response_model=AccountingPeriodRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create an accounting period",

)

def create_accounting_period(

    payload: AccountingPeriodCreate, db: DbDep, business_id: BusinessDep

) -> AccountingPeriodRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get(

    "", response_model=AccountingPeriodListResponse, summary="List accounting periods"

)

def list_accounting_periods(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_disabled: bool = Query(default=True),

) -> AccountingPeriodListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_disabled=include_disabled,

    )

    return AccountingPeriodListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{period_id}", response_model=AccountingPeriodRead, summary="Get one accounting period"

)

def get_accounting_period(

    period_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> AccountingPeriodRead:

    try:

        return _read(_service.get(db, business_id, period_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{period_id}", response_model=AccountingPeriodRead, summary="Update an accounting period"

)

def update_accounting_period(

    period_id: uuid.UUID,

    payload: AccountingPeriodUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> AccountingPeriodRead:

    try:

        return _read(_service.update(db, business_id, period_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{period_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete an accounting period",

)

def delete_accounting_period(

    period_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, period_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
