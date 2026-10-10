"""HTTP surface for Dunning Type."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.dunning_type_domain.schemas.dunning_type import (

    DunningTypeCreate,

    DunningTypeListResponse,

    DunningTypeRead,

    DunningTypeUpdate,

)

from app.accounts.dunning_type_domain.services.dunning_type_service import DunningTypeService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = DunningTypeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=DunningTypeRead, status_code=status.HTTP_201_CREATED,

    summary="Create a dunning type",

)

def create_dunning_type(

    payload: DunningTypeCreate, db: DbDep, business_id: BusinessDep

) -> DunningTypeRead:

    try:

        return DunningTypeRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=DunningTypeListResponse, summary="List dunning types")

def list_dunning_types(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> DunningTypeListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return DunningTypeListResponse.from_result(

        page, [DunningTypeRead.model_validate(r) for r in page.items]

    )





@router.get("/{dunning_type_id}", response_model=DunningTypeRead, summary="Get one dunning type")

def get_dunning_type(

    dunning_type_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> DunningTypeRead:

    try:

        return DunningTypeRead.model_validate(_service.get(db, business_id, dunning_type_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{dunning_type_id}", response_model=DunningTypeRead, summary="Update")

def update_dunning_type(

    dunning_type_id: uuid.UUID, payload: DunningTypeUpdate, db: DbDep,

    business_id: BusinessDep,

) -> DunningTypeRead:

    try:

        return DunningTypeRead.model_validate(

            _service.update(db, business_id, dunning_type_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{dunning_type_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete"

)

def delete_dunning_type(

    dunning_type_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, dunning_type_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
