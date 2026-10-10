"""HTTP surface for Mode of Payment."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.mode_of_payment_domain.models.mode_of_payment import ModeOfPaymentType

from app.accounts.mode_of_payment_domain.schemas.mode_of_payment import (

    ModeOfPaymentCreate,

    ModeOfPaymentListResponse,

    ModeOfPaymentRead,

    ModeOfPaymentUpdate,

)

from app.accounts.mode_of_payment_domain.services.mode_of_payment_service import (

    ModeOfPaymentService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ModeOfPaymentService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=ModeOfPaymentRead, status_code=status.HTTP_201_CREATED,

    summary="Create a mode of payment",

)

def create_mode_of_payment(

    payload: ModeOfPaymentCreate, db: DbDep, business_id: BusinessDep

) -> ModeOfPaymentRead:

    try:

        return ModeOfPaymentRead.model_validate(

            _service.create(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=ModeOfPaymentListResponse, summary="List modes of payment")

def list_modes_of_payment(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    include_disabled: bool = Query(default=True),

    type: Optional[ModeOfPaymentType] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

) -> ModeOfPaymentListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        include_disabled=include_disabled, type=type, search=search,

    )

    return ModeOfPaymentListResponse.from_result(

        page, [ModeOfPaymentRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ModeOfPaymentRead, summary="Get one mode of payment"

)

def get_mode_of_payment(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ModeOfPaymentRead:

    try:

        return ModeOfPaymentRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=ModeOfPaymentRead, summary="Update")

def update_mode_of_payment(

    row_id: uuid.UUID, payload: ModeOfPaymentUpdate, db: DbDep, business_id: BusinessDep

) -> ModeOfPaymentRead:

    try:

        return ModeOfPaymentRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_mode_of_payment(

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
