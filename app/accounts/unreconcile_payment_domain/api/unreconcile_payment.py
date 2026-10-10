"""HTTP surface for Unreconcile Payment."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.unreconcile_payment_domain.schemas.unreconcile_payment import (

        UnreconcilePaymentCreate,

    UnreconcilePaymentUpdate,

    UnreconcilePaymentRead,

    UnreconcilePaymentListResponse,

)

from app.accounts.unreconcile_payment_domain.services.unreconcile_payment_service import UnreconcilePaymentService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = UnreconcilePaymentService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=UnreconcilePaymentRead, status_code=status.HTTP_201_CREATED,

    summary="Create a unreconcile payment",

)

def create_unreconcile_payment(

    payload: UnreconcilePaymentCreate, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentRead:

    try:

        return UnreconcilePaymentRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=UnreconcilePaymentListResponse, summary="List unreconcile payments")

def list_unreconcile_payment(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> UnreconcilePaymentListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return UnreconcilePaymentListResponse.from_result(

        page, [UnreconcilePaymentRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=UnreconcilePaymentRead, summary="Get one unreconcile payment"

)

def get_unreconcile_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentRead:

    try:

        return UnreconcilePaymentRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=UnreconcilePaymentRead, summary="Update")

def update_unreconcile_payment(

    row_id: uuid.UUID, payload: UnreconcilePaymentUpdate, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentRead:

    try:

        return UnreconcilePaymentRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_unreconcile_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to NoneType and then rejects for a

    # 204 at import time.

    try:

        _service.delete(db, business_id, row_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post("/{row_id}/submit", response_model=UnreconcilePaymentRead, summary="Submit")

def submit_unreconcile_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentRead:

    try:

        return UnreconcilePaymentRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=UnreconcilePaymentRead, summary="Cancel")

def cancel_unreconcile_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> UnreconcilePaymentRead:

    try:

        return UnreconcilePaymentRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
