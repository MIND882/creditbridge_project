"""HTTP surface for Accounting Dimension Filter."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_filter_domain.schemas.accounting_dimension_filter import (

    AccountingDimensionFilterCreate,

    AccountingDimensionFilterListResponse,

    AccountingDimensionFilterRead,

    AccountingDimensionFilterUpdate,

)

from app.accounts.accounting_dimension_filter_domain.services.accounting_dimension_filter_service import (

    AccountingDimensionFilterService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AccountingDimensionFilterService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> AccountingDimensionFilterRead:

    return AccountingDimensionFilterRead.model_validate(row)





@router.post(

    "",

    response_model=AccountingDimensionFilterRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a dimension filter",

)

def create_dimension_filter(

    payload: AccountingDimensionFilterCreate, db: DbDep, business_id: BusinessDep

) -> AccountingDimensionFilterRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=AccountingDimensionFilterListResponse, summary="List filters")

def list_dimension_filters(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    accounting_dimension: Optional[str] = Query(default=None, max_length=140),

    include_disabled: bool = Query(default=True),

) -> AccountingDimensionFilterListResponse:

    page = _service.list(

        db,

        business_id,

        offset=offset,

        limit=limit,

        accounting_dimension=accounting_dimension,

        include_disabled=include_disabled,

    )

    return AccountingDimensionFilterListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{filter_id}", response_model=AccountingDimensionFilterRead, summary="Get one filter"

)

def get_dimension_filter(

    filter_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> AccountingDimensionFilterRead:

    try:

        return _read(_service.get(db, business_id, filter_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{filter_id}", response_model=AccountingDimensionFilterRead, summary="Update a filter"

)

def update_dimension_filter(

    filter_id: uuid.UUID,

    payload: AccountingDimensionFilterUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> AccountingDimensionFilterRead:

    try:

        return _read(_service.update(db, business_id, filter_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{filter_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a filter",

)

def delete_dimension_filter(

    filter_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, filter_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
