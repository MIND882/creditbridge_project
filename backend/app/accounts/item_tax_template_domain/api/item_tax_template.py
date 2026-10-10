"""HTTP surface for Item Tax Template."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.item_tax_template_domain.schemas.item_tax_template import (

    ItemTaxTemplateCreate,

    ItemTaxTemplateListResponse,

    ItemTaxTemplateRead,

    ItemTaxTemplateUpdate,

)

from app.accounts.item_tax_template_domain.services.item_tax_template_service import (

    ItemTaxTemplateService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ItemTaxTemplateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=ItemTaxTemplateRead, status_code=status.HTTP_201_CREATED,

    summary="Create an item tax template",

)

def create_item_tax_template(

    payload: ItemTaxTemplateCreate, db: DbDep, business_id: BusinessDep

) -> ItemTaxTemplateRead:

    try:

        return ItemTaxTemplateRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=ItemTaxTemplateListResponse, summary="List item tax templates")

def list_item_tax_templates(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    include_disabled: bool = Query(default=True),

    search: Optional[str] = Query(default=None, max_length=140),

) -> ItemTaxTemplateListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        include_disabled=include_disabled, search=search,

    )

    return ItemTaxTemplateListResponse.from_result(

        page, [ItemTaxTemplateRead.model_validate(r) for r in page.items]

    )





@router.get("/{template_id}", response_model=ItemTaxTemplateRead, summary="Get one template")

def get_item_tax_template(

    template_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ItemTaxTemplateRead:

    try:

        return ItemTaxTemplateRead.model_validate(_service.get(db, business_id, template_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{template_id}", response_model=ItemTaxTemplateRead, summary="Update")

def update_item_tax_template(

    template_id: uuid.UUID, payload: ItemTaxTemplateUpdate, db: DbDep,

    business_id: BusinessDep,

) -> ItemTaxTemplateRead:

    try:

        return ItemTaxTemplateRead.model_validate(

            _service.update(db, business_id, template_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{template_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete"

)

def delete_item_tax_template(

    template_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, template_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
