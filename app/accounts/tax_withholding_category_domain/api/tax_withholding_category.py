"""HTTP surface for Tax Withholding Category."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_category_domain.schemas.tax_withholding_category import (

    TaxWithholdingCategoryCreate,

    TaxWithholdingCategoryListResponse,

    TaxWithholdingCategoryRead,

    TaxWithholdingCategoryUpdate,

)

from app.accounts.tax_withholding_category_domain.services.tax_withholding_category_service import (

    TaxWithholdingCategoryService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxWithholdingCategoryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=TaxWithholdingCategoryRead, status_code=status.HTTP_201_CREATED,

    summary="Create a tax withholding category",

)

def create_category(

    payload: TaxWithholdingCategoryCreate, db: DbDep, business_id: BusinessDep

) -> TaxWithholdingCategoryRead:

    try:

        return TaxWithholdingCategoryRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=TaxWithholdingCategoryListResponse, summary="List categories")

def list_categories(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> TaxWithholdingCategoryListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return TaxWithholdingCategoryListResponse.from_result(

        page, [TaxWithholdingCategoryRead.model_validate(r) for r in page.items]

    )





@router.get("/{category_id}", response_model=TaxWithholdingCategoryRead, summary="Get one")

def get_category(

    category_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> TaxWithholdingCategoryRead:

    try:

        return TaxWithholdingCategoryRead.model_validate(

            _service.get(db, business_id, category_id)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{category_id}", response_model=TaxWithholdingCategoryRead, summary="Update")

def update_category(

    category_id: uuid.UUID, payload: TaxWithholdingCategoryUpdate, db: DbDep,

    business_id: BusinessDep,

) -> TaxWithholdingCategoryRead:

    try:

        return TaxWithholdingCategoryRead.model_validate(

            _service.update(db, business_id, category_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a category"

)

def delete_category(category_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

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
