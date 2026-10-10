"""HTTP surface for Purchase Taxes and Charges Template."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.purchase_taxes_and_charges_template_domain.schemas.purchase_taxes_and_charges_template import (  # noqa: E501

    PurchaseTaxesAndChargesTemplateCreate,

    PurchaseTaxesAndChargesTemplateListResponse,

    PurchaseTaxesAndChargesTemplateRead,

    PurchaseTaxesAndChargesTemplateUpdate,

)

from app.accounts.purchase_taxes_and_charges_template_domain.services.purchase_taxes_and_charges_template_service import (  # noqa: E501

    PurchaseTaxesAndChargesTemplateService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PurchaseTaxesAndChargesTemplateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=PurchaseTaxesAndChargesTemplateRead,

    status_code=status.HTTP_201_CREATED,

    summary="Create a purchase tax template",

)

def create_template(

    payload: PurchaseTaxesAndChargesTemplateCreate, db: DbDep, business_id: BusinessDep

) -> PurchaseTaxesAndChargesTemplateRead:

    try:

        return PurchaseTaxesAndChargesTemplateRead.model_validate(

            _service.create(db, business_id, payload)

        )

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PurchaseTaxesAndChargesTemplateListResponse, summary="List")

def list_templates(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    include_disabled: bool = Query(default=True),

    tax_category_id: Optional[uuid.UUID] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

) -> PurchaseTaxesAndChargesTemplateListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        include_disabled=include_disabled, tax_category_id=tax_category_id, search=search,

    )

    return PurchaseTaxesAndChargesTemplateListResponse.from_result(

        page, [PurchaseTaxesAndChargesTemplateRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{template_id}", response_model=PurchaseTaxesAndChargesTemplateRead, summary="Get one"

)

def get_template(

    template_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PurchaseTaxesAndChargesTemplateRead:

    try:

        return PurchaseTaxesAndChargesTemplateRead.model_validate(

            _service.get(db, business_id, template_id)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch(

    "/{template_id}", response_model=PurchaseTaxesAndChargesTemplateRead, summary="Update"

)

def update_template(

    template_id: uuid.UUID, payload: PurchaseTaxesAndChargesTemplateUpdate, db: DbDep,

    business_id: BusinessDep,

) -> PurchaseTaxesAndChargesTemplateRead:

    try:

        return PurchaseTaxesAndChargesTemplateRead.model_validate(

            _service.update(db, business_id, template_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{template_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete"

)

def delete_template(template_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

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
