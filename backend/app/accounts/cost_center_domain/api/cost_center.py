"""

HTTP surface for Cost Center.



``/tree`` and ``/parent-options`` are declared before ``/{cost_center_id}`` so

the literal segments win over the path parameter.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.cost_center_domain.schemas.cost_center import (

    CostCenterConvertResult,

    CostCenterCreate,

    CostCenterListResponse,

    CostCenterRead,

    CostCenterTreeResponse,

    CostCenterUpdate,

)

from app.accounts.cost_center_domain.services.cost_center_service import CostCenterService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = CostCenterService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> CostCenterRead:

    return CostCenterRead.model_validate(row)





@router.post(

    "",

    response_model=CostCenterRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a cost center",

)

def create_cost_center(

    payload: CostCenterCreate, db: DbDep, business_id: BusinessDep

) -> CostCenterRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=CostCenterListResponse, summary="List cost centers")

def list_cost_centers(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    is_group: Optional[bool] = Query(default=None),

    include_disabled: bool = Query(default=True),

    parent_cost_center_id: Optional[uuid.UUID] = Query(default=None),

    roots_only: bool = Query(default=False),

) -> CostCenterListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        search=search,

        is_group=is_group,

        include_disabled=include_disabled,

        parent_cost_center_id=parent_cost_center_id,

        roots_only=roots_only,

    )

    return CostCenterListResponse.from_result(page, [_read(r) for r in page.items])





@router.get("/tree", response_model=CostCenterTreeResponse, summary="Nested cost center tree")

def get_cost_center_tree(db: DbDep, business_id: BusinessDep) -> CostCenterTreeResponse:

    roots, total = _service.get_tree(db, business_id)

    return CostCenterTreeResponse(roots=roots, total_nodes=total)





@router.get(

    "/parent-options",

    response_model=list[CostCenterRead],

    summary="Group cost centers usable as a parent",

)

def list_cost_center_parent_options(

    db: DbDep,

    business_id: BusinessDep,

    search: Optional[str] = Query(default=None, max_length=140),

) -> list[CostCenterRead]:

    return [_read(r) for r in _service.list_parent_options(db, business_id, search=search)]





@router.get(

    "/{cost_center_id}", response_model=CostCenterRead, summary="Get one cost center"

)

def get_cost_center(

    cost_center_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CostCenterRead:

    try:

        return _read(_service.get(db, business_id, cost_center_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{cost_center_id}", response_model=CostCenterRead, summary="Update a cost center"

)

def update_cost_center(

    cost_center_id: uuid.UUID,

    payload: CostCenterUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> CostCenterRead:

    try:

        return _read(_service.update(db, business_id, cost_center_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{cost_center_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a cost center",

)

def delete_cost_center(

    cost_center_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, cost_center_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.post(

    "/{cost_center_id}/convert_to_ledger",

    response_model=CostCenterConvertResult,

    summary="Convert a group cost center to a ledger",

)

def convert_cost_center_to_ledger(

    cost_center_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CostCenterConvertResult:

    try:

        row = _service.convert_to_ledger(db, business_id, cost_center_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return CostCenterConvertResult(id=row.id, is_group=row.is_group)





@router.post(

    "/{cost_center_id}/convert_to_group",

    response_model=CostCenterConvertResult,

    summary="Convert a ledger cost center to a group",

)

def convert_cost_center_to_group(

    cost_center_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> CostCenterConvertResult:

    try:

        row = _service.convert_to_group(db, business_id, cost_center_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return CostCenterConvertResult(id=row.id, is_group=row.is_group)
