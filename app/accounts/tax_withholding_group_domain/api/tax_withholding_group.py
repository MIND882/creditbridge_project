"""HTTP surface for Tax Withholding Group."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_group_domain.schemas.tax_withholding_group import (

        TaxWithholdingGroupCreate,

    TaxWithholdingGroupUpdate,

    TaxWithholdingGroupRead,

    TaxWithholdingGroupListResponse,

)

from app.accounts.tax_withholding_group_domain.services.tax_withholding_group_service import TaxWithholdingGroupService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxWithholdingGroupService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=TaxWithholdingGroupRead, status_code=status.HTTP_201_CREATED,

    summary="Create a tax withholding group",

)

def create_tax_withholding_group(

    payload: TaxWithholdingGroupCreate, db: DbDep, business_id: BusinessDep

) -> TaxWithholdingGroupRead:

    try:

        return TaxWithholdingGroupRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=TaxWithholdingGroupListResponse, summary="List tax withholding groups")

def list_tax_withholding_group(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> TaxWithholdingGroupListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

    )

    return TaxWithholdingGroupListResponse.from_result(

        page, [TaxWithholdingGroupRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=TaxWithholdingGroupRead, summary="Get one tax withholding group"

)

def get_tax_withholding_group(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> TaxWithholdingGroupRead:

    try:

        return TaxWithholdingGroupRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=TaxWithholdingGroupRead, summary="Update")

def update_tax_withholding_group(

    row_id: uuid.UUID, payload: TaxWithholdingGroupUpdate, db: DbDep, business_id: BusinessDep

) -> TaxWithholdingGroupRead:

    try:

        return TaxWithholdingGroupRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_tax_withholding_group(

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
