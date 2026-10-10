"""HTTP surface for Tax Category."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.tax_category_domain.schemas.tax_category import (

    TaxCategoryCreate,

    TaxCategoryListResponse,

    TaxCategoryRead,

    TaxCategoryUpdate,

)

from app.accounts.tax_category_domain.services.tax_category_service import TaxCategoryService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxCategoryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=TaxCategoryRead, status_code=status.HTTP_201_CREATED,

    summary="Create a tax category",

)

def create_tax_category(

    payload: TaxCategoryCreate, db: DbDep, business_id: BusinessDep

) -> TaxCategoryRead:

    try:

        return TaxCategoryRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=TaxCategoryListResponse, summary="List tax categories")

def list_tax_categories(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    include_disabled: bool = Query(default=True),

    search: Optional[str] = Query(default=None, max_length=140),

) -> TaxCategoryListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        include_disabled=include_disabled, search=search,

    )

    return TaxCategoryListResponse.from_result(

        page, [TaxCategoryRead.model_validate(r) for r in page.items]

    )





@router.get("/{category_id}", response_model=TaxCategoryRead, summary="Get one tax category")

def get_tax_category(

    category_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> TaxCategoryRead:

    try:

        return TaxCategoryRead.model_validate(_service.get(db, business_id, category_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{category_id}", response_model=TaxCategoryRead, summary="Update")

def update_tax_category(

    category_id: uuid.UUID, payload: TaxCategoryUpdate, db: DbDep, business_id: BusinessDep

) -> TaxCategoryRead:

    try:

        return TaxCategoryRead.model_validate(

            _service.update(db, business_id, category_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete"

)

def delete_tax_category(category_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, category_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
