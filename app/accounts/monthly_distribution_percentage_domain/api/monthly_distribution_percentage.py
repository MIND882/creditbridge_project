"""HTTP surface for Monthly Distribution Percentage -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.monthly_distribution_percentage_domain.schemas.monthly_distribution_percentage import (

    MonthlyDistributionPercentageListResponse,

    MonthlyDistributionPercentageRead,

)

from app.accounts.monthly_distribution_percentage_domain.services.monthly_distribution_percentage_service import MonthlyDistributionPercentageService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = MonthlyDistributionPercentageService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=MonthlyDistributionPercentageListResponse, summary="List monthly distribution percentage rows")

def list_monthly_distribution_percentage(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> MonthlyDistributionPercentageListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return MonthlyDistributionPercentageListResponse.from_result(

        page, [MonthlyDistributionPercentageRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=MonthlyDistributionPercentageRead, summary="Get one monthly distribution percentage row")

def get_monthly_distribution_percentage(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> MonthlyDistributionPercentageRead:

    try:

        return MonthlyDistributionPercentageRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
