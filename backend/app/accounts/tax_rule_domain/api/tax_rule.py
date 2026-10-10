"""HTTP surface for Tax Rule."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from sqlalchemy.orm import Session



from app.accounts.tax_enums import TaxRuleType

from app.accounts.tax_rule_domain.schemas.tax_rule import (

    TaxRuleCreate,

    TaxRuleListResponse,

    TaxRuleRead,

    TaxRuleUpdate,

)

from app.accounts.tax_rule_domain.services.tax_rule_service import TaxRuleService

from app.core.errors import DomainValidationError, NotFoundError, to_http_exception

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = TaxRuleService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.post(

    "", response_model=TaxRuleRead, status_code=status.HTTP_201_CREATED,

    summary="Create a tax rule",

)

def create_tax_rule(

    payload: TaxRuleCreate, db: DbDep, business_id: BusinessDep

) -> TaxRuleRead:

    try:

        return TaxRuleRead.model_validate(_service.create(db, business_id, payload))

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.get("", response_model=TaxRuleListResponse, summary="List tax rules")

def list_tax_rules(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    tax_type: Optional[TaxRuleType] = Query(default=None),

    tax_category_id: Optional[uuid.UUID] = Query(default=None),

    search: Optional[str] = Query(default=None, max_length=140),

) -> TaxRuleListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        tax_type=tax_type.value if tax_type else None,

        tax_category_id=tax_category_id, search=search,

    )

    return TaxRuleListResponse.from_result(

        page, [TaxRuleRead.model_validate(r) for r in page.items]

    )





@router.get("/{rule_id}", response_model=TaxRuleRead, summary="Get one tax rule")

def get_tax_rule(rule_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> TaxRuleRead:

    try:

        return TaxRuleRead.model_validate(_service.get(db, business_id, rule_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc





@router.patch("/{rule_id}", response_model=TaxRuleRead, summary="Update a tax rule")

def update_tax_rule(

    rule_id: uuid.UUID, payload: TaxRuleUpdate, db: DbDep, business_id: BusinessDep

) -> TaxRuleRead:

    try:

        return TaxRuleRead.model_validate(_service.update(db, business_id, rule_id, payload))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc





@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete")

def delete_tax_rule(rule_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> Response:

    # `-> Response` not `-> None`: under PEP 563 the annotation becomes the

    # string "None", which FastAPI resolves to the truthy NoneType class and

    # then rejects for a 204 at import time.

    try:

        _service.delete(db, business_id, rule_id)

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    except DomainValidationError as exc:

        raise to_http_exception(exc) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
