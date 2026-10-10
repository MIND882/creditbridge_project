"""HTTP surface for Pricing Rule Brand -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_brand_domain.schemas.pricing_rule_brand import (

    PricingRuleBrandListResponse,

    PricingRuleBrandRead,

)

from app.accounts.pricing_rule_brand_domain.services.pricing_rule_brand_service import PricingRuleBrandService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PricingRuleBrandService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PricingRuleBrandListResponse, summary="List pricing rule brand rows")

def list_pricing_rule_brand(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PricingRuleBrandListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PricingRuleBrandListResponse.from_result(

        page, [PricingRuleBrandRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PricingRuleBrandRead, summary="Get one pricing rule brand row")

def get_pricing_rule_brand(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PricingRuleBrandRead:

    try:

        return PricingRuleBrandRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
