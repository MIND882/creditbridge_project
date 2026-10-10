"""HTTP surface for Sales Partner Type."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.selling.sales_partner_type_domain.schemas.sales_partner_type import (

    SalesPartnerTypeCreate,

    SalesPartnerTypeUpdate,

    SalesPartnerTypeRead,

    SalesPartnerTypeListResponse,

)

from app.selling.sales_partner_type_domain.services.sales_partner_type_service import SalesPartnerTypeService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = SalesPartnerTypeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=SalesPartnerTypeRead, status_code=status.HTTP_201_CREATED,

    summary="Create a sales partner type",

)

def create_sales_partner_type(

    payload: SalesPartnerTypeCreate, db: DbDep, business_id: BusinessDep

) -> SalesPartnerTypeRead:

    try:

        return SalesPartnerTypeRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=SalesPartnerTypeListResponse, summary="List sales partner types")

def list_sales_partner_type(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

    include_cancelled: bool = Query(default=False),

) -> SalesPartnerTypeListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, search=search,

        include_cancelled=include_cancelled,

    )

    return SalesPartnerTypeListResponse.from_result(

        page, [SalesPartnerTypeRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=SalesPartnerTypeRead, summary="Get one sales partner type"

)

def get_sales_partner_type(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> SalesPartnerTypeRead:

    try:

        return SalesPartnerTypeRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{row_id}", response_model=SalesPartnerTypeRead, summary="Update")

def update_sales_partner_type(

    row_id: uuid.UUID, payload: SalesPartnerTypeUpdate, db: DbDep, business_id: BusinessDep

) -> SalesPartnerTypeRead:

    try:

        return SalesPartnerTypeRead.model_validate(

            _service.update(db, business_id, row_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{row_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_sales_partner_type(

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
