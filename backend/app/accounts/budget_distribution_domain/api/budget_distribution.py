"""HTTP surface for Budget Distribution -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.budget_distribution_domain.schemas.budget_distribution import (

    BudgetDistributionListResponse,

    BudgetDistributionRead,

)

from app.accounts.budget_distribution_domain.services.budget_distribution_service import BudgetDistributionService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BudgetDistributionService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=BudgetDistributionListResponse, summary="List budget distribution rows")

def list_budget_distribution(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BudgetDistributionListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return BudgetDistributionListResponse.from_result(

        page, [BudgetDistributionRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=BudgetDistributionRead, summary="Get one budget distribution row")

def get_budget_distribution(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BudgetDistributionRead:

    try:

        return BudgetDistributionRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
