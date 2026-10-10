"""HTTP surface for Bank Account."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_account_domain.schemas.bank_account import (

    BankAccountCreate,

    BankAccountListResponse,

    BankAccountRead,

    BankAccountUpdate,

)

from app.accounts.bank_account_domain.services.bank_account_service import BankAccountService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankAccountRead:

    return BankAccountRead.model_validate(row)





@router.post(

    "",

    response_model=BankAccountRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a bank account",

)

def create_bank_account(

    payload: BankAccountCreate, db: DbDep, business_id: BusinessDep

) -> BankAccountRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankAccountListResponse, summary="List bank accounts")

def list_bank_accounts(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    bank_id: Optional[uuid.UUID] = Query(default=None),

    is_company_account: Optional[bool] = Query(default=None),

    include_disabled: bool = Query(default=True),

) -> BankAccountListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        search=search,

        bank_id=bank_id,

        is_company_account=is_company_account,

        include_disabled=include_disabled,

    )

    return BankAccountListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{bank_account_id}", response_model=BankAccountRead, summary="Get one bank account"

)

def get_bank_account(

    bank_account_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BankAccountRead:

    try:

        return _read(_service.get(db, business_id, bank_account_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{bank_account_id}", response_model=BankAccountRead, summary="Update a bank account"

)

def update_bank_account(

    bank_account_id: uuid.UUID,

    payload: BankAccountUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> BankAccountRead:

    try:

        return _read(_service.update(db, business_id, bank_account_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{bank_account_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a bank account",

)

def delete_bank_account(

    bank_account_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, bank_account_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
