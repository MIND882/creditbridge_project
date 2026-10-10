"""HTTP surface for Bank."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.bank_domain.schemas.bank import (

    BankCreate,

    BankListResponse,

    BankRead,

    BankUpdate,

)

from app.accounts.bank_domain.services.bank_service import BankService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BankService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> BankRead:

    return BankRead.model_validate(row)





@router.post(

    "", response_model=BankRead, status_code=status.HTTP_201_CREATED, summary="Create a bank"

)

def create_bank(payload: BankCreate, db: DbDep, business_id: BusinessDep) -> BankRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=BankListResponse, summary="List banks")

def list_banks(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> BankListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return BankListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{bank_id}", response_model=BankRead, summary="Get one bank")

def get_bank(bank_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> BankRead:

    try:

        return _read(_service.get(db, business_id, bank_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{bank_id}", response_model=BankRead, summary="Update a bank")

def update_bank(

    bank_id: uuid.UUID, payload: BankUpdate, db: DbDep, business_id: BusinessDep

) -> BankRead:

    try:

        return _read(_service.update(db, business_id, bank_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{bank_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a bank"

)

def delete_bank(bank_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, bank_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
