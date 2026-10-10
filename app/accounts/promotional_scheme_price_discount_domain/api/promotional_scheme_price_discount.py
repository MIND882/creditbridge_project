"""HTTP surface for Promotional Scheme Price Discount -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_price_discount_domain.schemas.promotional_scheme_price_discount import (

    PromotionalSchemePriceDiscountListResponse,

    PromotionalSchemePriceDiscountRead,

)

from app.accounts.promotional_scheme_price_discount_domain.services.promotional_scheme_price_discount_service import PromotionalSchemePriceDiscountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PromotionalSchemePriceDiscountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PromotionalSchemePriceDiscountListResponse, summary="List promotional scheme price discount rows")

def list_promotional_scheme_price_discount(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PromotionalSchemePriceDiscountListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PromotionalSchemePriceDiscountListResponse.from_result(

        page, [PromotionalSchemePriceDiscountRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PromotionalSchemePriceDiscountRead, summary="Get one promotional scheme price discount row")

def get_promotional_scheme_price_discount(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PromotionalSchemePriceDiscountRead:

    try:

        return PromotionalSchemePriceDiscountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
