"""HTTP surface for Shipping Rule Condition -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.shipping_rule_condition_domain.schemas.shipping_rule_condition import (

    ShippingRuleConditionListResponse,

    ShippingRuleConditionRead,

)

from app.accounts.shipping_rule_condition_domain.services.shipping_rule_condition_service import ShippingRuleConditionService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ShippingRuleConditionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ShippingRuleConditionListResponse, summary="List shipping rule condition rows")

def list_shipping_rule_condition(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ShippingRuleConditionListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ShippingRuleConditionListResponse.from_result(

        page, [ShippingRuleConditionRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=ShippingRuleConditionRead, summary="Get one shipping rule condition row")

def get_shipping_rule_condition(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ShippingRuleConditionRead:

    try:

        return ShippingRuleConditionRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
