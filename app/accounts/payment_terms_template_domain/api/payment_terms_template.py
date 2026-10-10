"""HTTP surface for Payment Terms Template."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.payment_terms_template_domain.schemas.payment_terms_template import (

    PaymentTermsTemplateCreate,

    PaymentTermsTemplateListResponse,

    PaymentTermsTemplateRead,

    PaymentTermsTemplateUpdate,

)

from app.accounts.payment_terms_template_domain.services.payment_terms_template_service import (

    PaymentTermsTemplateService,

)

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PaymentTermsTemplateService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=PaymentTermsTemplateRead, status_code=status.HTTP_201_CREATED,

    summary="Create a payment terms template",

)

def create_template(

    payload: PaymentTermsTemplateCreate, db: DbDep, business_id: BusinessDep

) -> PaymentTermsTemplateRead:

    try:

        return PaymentTermsTemplateRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=PaymentTermsTemplateListResponse, summary="List templates")

def list_templates(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    search: Optional[str] = Query(default=None, max_length=140),

) -> PaymentTermsTemplateListResponse:

    page = _service.list(db, business_id, offset=offset, limit=limit, search=search)

    return PaymentTermsTemplateListResponse.from_result(

        page, [PaymentTermsTemplateRead.model_validate(r) for r in page.items]

    )





@router.get("/{template_id}", response_model=PaymentTermsTemplateRead, summary="Get one template")

def get_template(

    template_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PaymentTermsTemplateRead:

    try:

        return PaymentTermsTemplateRead.model_validate(

            _service.get(db, business_id, template_id)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{template_id}", response_model=PaymentTermsTemplateRead, summary="Update")

def update_template(

    template_id: uuid.UUID, payload: PaymentTermsTemplateUpdate, db: DbDep,

    business_id: BusinessDep,

) -> PaymentTermsTemplateRead:

    try:

        return PaymentTermsTemplateRead.model_validate(

            _service.update(db, business_id, template_id, payload)

        )

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete(

    "/{template_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a template"

)

def delete_template(

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
