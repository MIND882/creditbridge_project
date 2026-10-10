"""HTTP surface for Payment Term."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.payment_term_domain.schemas.payment_term import (

    PaymentTermCreate,

    PaymentTermListResponse,

    PaymentTermRead,

    PaymentTermUpdate,

)

from app.accounts.payment_term_domain.services.payment_term_service import PaymentTermService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentTermService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=PaymentTermRead, status_code=status.HTTP_201_CREATED,

    summary="Create a payment term",

)

def create_payment_term(

    payload: PaymentTermCreate, db: DbDep, business_id: BusinessDep

) -> PaymentTermRead:

    try:

        return PaymentTermRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PaymentTermListResponse, summary="List payment terms")

def list_payment_terms(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> PaymentTermListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return PaymentTermListResponse.from_result(

        page, [PaymentTermRead.model_validate(r) for r in page.items]

    )





@router.get("/{term_id}", response_model=PaymentTermRead, summary="Get one payment term")

def get_payment_term(term_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> PaymentTermRead:

    try:

        return PaymentTermRead.model_validate(_service.get(db, business_id, term_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{term_id}", response_model=PaymentTermRead, summary="Update a payment term")

def update_payment_term(

    term_id: uuid.UUID, payload: PaymentTermUpdate, db: DbDep, business_id: BusinessDep

) -> PaymentTermRead:

    try:

        return PaymentTermRead.model_validate(_service.update(db, business_id, term_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{term_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a payment term"

)

def delete_payment_term(term_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, term_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
