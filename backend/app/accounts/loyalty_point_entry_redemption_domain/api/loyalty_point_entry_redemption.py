"""HTTP surface for Loyalty Point Entry Redemption -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.loyalty_point_entry_redemption_domain.schemas.loyalty_point_entry_redemption import (

    LoyaltyPointEntryRedemptionListResponse,

    LoyaltyPointEntryRedemptionRead,

)

from app.accounts.loyalty_point_entry_redemption_domain.services.loyalty_point_entry_redemption_service import LoyaltyPointEntryRedemptionService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = LoyaltyPointEntryRedemptionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=LoyaltyPointEntryRedemptionListResponse, summary="List loyalty point entry redemption rows")

def list_loyalty_point_entry_redemption(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> LoyaltyPointEntryRedemptionListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return LoyaltyPointEntryRedemptionListResponse.from_result(

        page, [LoyaltyPointEntryRedemptionRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=LoyaltyPointEntryRedemptionRead, summary="Get one loyalty point entry redemption row")

def get_loyalty_point_entry_redemption(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> LoyaltyPointEntryRedemptionRead:

    try:

        return LoyaltyPointEntryRedemptionRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
