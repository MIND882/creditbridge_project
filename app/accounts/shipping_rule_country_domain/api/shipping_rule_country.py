"""HTTP surface for Shipping Rule Country -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.shipping_rule_country_domain.schemas.shipping_rule_country import (

    ShippingRuleCountryListResponse,

    ShippingRuleCountryRead,

)

from app.accounts.shipping_rule_country_domain.services.shipping_rule_country_service import ShippingRuleCountryService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ShippingRuleCountryService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ShippingRuleCountryListResponse, summary="List shipping rule country rows")

def list_shipping_rule_country(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ShippingRuleCountryListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ShippingRuleCountryListResponse.from_result(

        page, [ShippingRuleCountryRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ShippingRuleCountryRead, summary="Get one shipping rule country row")

def get_shipping_rule_country(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ShippingRuleCountryRead:

    try:

        return ShippingRuleCountryRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
