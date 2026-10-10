"""HTTP surface for Accounting Dimension."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.accounting_dimension_domain.schemas.accounting_dimension import (

    AccountingDimensionCreate,

    AccountingDimensionListResponse,

    AccountingDimensionRead,

    AccountingDimensionUpdate,

)

from app.accounts.accounting_dimension_domain.services.accounting_dimension_service import (

    AccountingDimensionService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AccountingDimensionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> AccountingDimensionRead:

    return AccountingDimensionRead.model_validate(row)





@router.post(

    "",

    response_model=AccountingDimensionRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create an accounting dimension",

)

def create_accounting_dimension(

    payload: AccountingDimensionCreate, db: DbDep, business_id: BusinessDep

) -> AccountingDimensionRead:

    try:

        return _read(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=AccountingDimensionListResponse, summary="List dimensions")

def list_accounting_dimensions(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_disabled: bool = Query(default=True),

    enabled_only: bool = Query(

        default=False, description="Shortcut for the transaction-form picker"

    ),

) -> AccountingDimensionListResponse:

    if enabled_only:

        rows = _service.list_enabled(db, business_id)

        return AccountingDimensionListResponse(

            items=[_read(r) for r in rows],

            total=len(rows),

            offset=0,

            limit=len(rows),

            has_more=False,

        )



    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_disabled=include_disabled,

    )

    return AccountingDimensionListResponse.from_result(page, [_read(r) for r in page.items])





@router.get(

    "/{dimension_id}", response_model=AccountingDimensionRead, summary="Get one dimension"

)

def get_accounting_dimension(

    dimension_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> AccountingDimensionRead:

    try:

        return _read(_service.get(db, business_id, dimension_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{dimension_id}", response_model=AccountingDimensionRead, summary="Update a dimension"

)

def update_accounting_dimension(

    dimension_id: uuid.UUID,

    payload: AccountingDimensionUpdate,

    db: DbDep,

    business_id: BusinessDep,

) -> AccountingDimensionRead:

    try:

        return _read(_service.update(db, business_id, dimension_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{dimension_id}",

    status_code=status.HTTP_204_NO_CONTENT,

    summary="Delete a dimension",

)

def delete_accounting_dimension(

    dimension_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, dimension_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
