"""HTTP surface for Cashier Closing."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.cashier_closing_domain.schemas.cashier_closing import (

        CashierClosingCreate,

    CashierClosingUpdate,

    CashierClosingRead,

    CashierClosingListResponse,

)

from app.accounts.cashier_closing_domain.services.cashier_closing_service import CashierClosingService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CashierClosingService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=CashierClosingRead, status_code=status.HTTP_201_CREATED,

    summary="Create a cashier closing",

)

def create_cashier_closing(

    payload: CashierClosingCreate, db: DbDep, business_id: BusinessDep

) -> CashierClosingRead:

    try:

        return CashierClosingRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=CashierClosingListResponse, summary="List cashier closings")

def list_cashier_closing(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> CashierClosingListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return CashierClosingListResponse.from_result(

        page, [CashierClosingRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=CashierClosingRead, summary="Get one cashier closing"

)

def get_cashier_closing(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CashierClosingRead:

    try:

        return CashierClosingRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=CashierClosingRead, summary="Update")

def update_cashier_closing(

    row_id: uuid.UUID, payload: CashierClosingUpdate, db: DbDep, business_id: BusinessDep

) -> CashierClosingRead:

    try:

        return CashierClosingRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_cashier_closing(

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





@router.post("/{row_id}/submit", response_model=CashierClosingRead, summary="Submit")

def submit_cashier_closing(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CashierClosingRead:

    try:

        return CashierClosingRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=CashierClosingRead, summary="Cancel")

def cancel_cashier_closing(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CashierClosingRead:

    try:

        return CashierClosingRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
