"""HTTP surface for Bank Account Type."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_account_type_domain.schemas.bank_account_type import (

    BankAccountTypeCreate, BankAccountTypeListResponse, BankAccountTypeRead, BankAccountTypeUpdate,

)

from app.accounts.bank_account_type_domain.services.bank_account_type_service import BankAccountTypeService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()

_service = BankAccountTypeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankAccountTypeRead:

    return BankAccountTypeRead.model_validate(row)





@router.post("", response_model=BankAccountTypeRead, status_code=status.HTTP_201_CREATED, summary="Create")

def create_row(payload: BankAccountTypeCreate, db: DbDep, business_id: BusinessDep) -> BankAccountTypeRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankAccountTypeListResponse, summary="List")

def list_rows(

    db: DbDep, business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> BankAccountTypeListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return BankAccountTypeListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{row_id}", response_model=BankAccountTypeRead, summary="Get one")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> BankAccountTypeRead:

    try:

        return _read(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=BankAccountTypeRead, summary="Update")

def update_row(row_id: uuid.UUID, payload: BankAccountTypeUpdate, db: DbDep, business_id: BusinessDep) -> BankAccountTypeRead:

    try:

        return _read(_service.update(db, business_id, row_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
