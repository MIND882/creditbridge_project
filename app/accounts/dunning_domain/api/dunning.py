"""HTTP surface for Dunning."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.dunning_domain.schemas.dunning import (

        DunningCreate,

    DunningUpdate,

    DunningRead,

    DunningListResponse,

)

from app.accounts.dunning_domain.services.dunning_service import DunningService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = DunningService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=DunningRead, status_code=status.HTTP_201_CREATED,

    summary="Create a dunning",

)

def create_dunning(

    payload: DunningCreate, db: DbDep, business_id: BusinessDep

) -> DunningRead:

    try:

        return DunningRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=DunningListResponse, summary="List dunnings")

def list_dunning(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> DunningListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return DunningListResponse.from_result(

        page, [DunningRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=DunningRead, summary="Get one dunning"

)

def get_dunning(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DunningRead:

    try:

        return DunningRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=DunningRead, summary="Update")

def update_dunning(

    row_id: uuid.UUID, payload: DunningUpdate, db: DbDep, business_id: BusinessDep

) -> DunningRead:

    try:

        return DunningRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_dunning(

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





@router.post("/{row_id}/submit", response_model=DunningRead, summary="Submit")

def submit_dunning(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DunningRead:

    try:

        return DunningRead.model_validate(_service.submit(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.post("/{row_id}/cancel", response_model=DunningRead, summary="Cancel")

def cancel_dunning(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DunningRead:

    try:

        return DunningRead.model_validate(_service.cancel(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc
