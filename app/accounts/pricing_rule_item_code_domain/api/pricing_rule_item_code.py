"""HTTP surface for Pricing Rule Item Code -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_item_code_domain.schemas.pricing_rule_item_code import (

    PricingRuleItemCodeListResponse,

    PricingRuleItemCodeRead,

)

from app.accounts.pricing_rule_item_code_domain.services.pricing_rule_item_code_service import PricingRuleItemCodeService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PricingRuleItemCodeService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PricingRuleItemCodeListResponse, summary="List pricing rule item code rows")

def list_pricing_rule_item_code(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PricingRuleItemCodeListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PricingRuleItemCodeListResponse.from_result(

        page, [PricingRuleItemCodeRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PricingRuleItemCodeRead, summary="Get one pricing rule item code row")

def get_pricing_rule_item_code(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PricingRuleItemCodeRead:

    try:

        return PricingRuleItemCodeRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
