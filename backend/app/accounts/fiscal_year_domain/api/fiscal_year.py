"""HTTP surface for Fiscal Year."""



from __future__ import annotations



import datetime as dt

import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.fiscal_year_domain.schemas.fiscal_year import (

    FiscalYearCreate,

    FiscalYearListResponse,

    FiscalYearRead,

    FiscalYearUpdate,

)

from app.accounts.fiscal_year_domain.services.fiscal_year_service import (

    FiscalYearService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = FiscalYearService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=FiscalYearRead, status_code=status.HTTP_201_CREATED,

    summary="Create a fiscal year",

)

def create_fiscal_year(

    payload: FiscalYearCreate, db: DbDep, business_id: BusinessDep

) -> FiscalYearRead:

    try:

        return FiscalYearRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=FiscalYearListResponse, summary="List fiscal years")

def list_fiscal_years(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    include_disabled: bool = Query(default=True),

    search: Optional[str] = Query(default=None, max_length=140),

) -> FiscalYearListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        include_disabled=include_disabled, search=search,

    )

    return FiscalYearListResponse.from_result(

        page, [FiscalYearRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/for-date", response_model=FiscalYearRead,

    summary="The fiscal year containing a date",

)

def get_fiscal_year_for_date(

    db: DbDep,

    business_id: BusinessDep,

    on: dt.date = Query(description="The date to look up"),

) -> FiscalYearRead:

    # Declared before "/{row_id}" so the literal path is not swallowed by the

    # parameterised route below it.

    #

    # `-> FiscalYearRead`, never `-> Optional[FiscalYearRead]`: under PEP 563 the

    # annotation is a string, and FastAPI building a TypeAdapter for a stringified

    # Optional[Model] raises "is not fully defined" at import time. A date with

    # no fiscal year is therefore a 404 rather than a 200 with a null body.

    row = _service.get_for_date(db, business_id, on)

    if row is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail=f"No fiscal year covers {on.isoformat()}",

        )

    return FiscalYearRead.model_validate(row)





@router.get("/{row_id}", response_model=FiscalYearRead, summary="Get one fiscal year")

def get_fiscal_year(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> FiscalYearRead:

    try:

        return FiscalYearRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=FiscalYearRead, summary="Update")

def update_fiscal_year(

    row_id: uuid.UUID, payload: FiscalYearUpdate, db: DbDep, business_id: BusinessDep

) -> FiscalYearRead:

    try:

        return FiscalYearRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_fiscal_year(

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
