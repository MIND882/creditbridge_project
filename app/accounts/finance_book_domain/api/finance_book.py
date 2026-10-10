"""HTTP surface for Finance Book."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.finance_book_domain.schemas.finance_book import (

    FinanceBookCreate, FinanceBookListResponse, FinanceBookRead, FinanceBookUpdate,

)

from app.accounts.finance_book_domain.services.finance_book_service import FinanceBookService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()

_service = FinanceBookService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> FinanceBookRead:

    return FinanceBookRead.model_validate(row)





@router.post("", response_model=FinanceBookRead, status_code=status.HTTP_201_CREATED, summary="Create")

def create_row(payload: FinanceBookCreate, db: DbDep, business_id: BusinessDep) -> FinanceBookRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=FinanceBookListResponse, summary="List")

def list_rows(

    db: DbDep, business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> FinanceBookListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return FinanceBookListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/{row_id}", response_model=FinanceBookRead, summary="Get one")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> FinanceBookRead:

    try:

        return _read(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=FinanceBookRead, summary="Update")

def update_row(row_id: uuid.UUID, payload: FinanceBookUpdate, db: DbDep, business_id: BusinessDep) -> FinanceBookRead:

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
