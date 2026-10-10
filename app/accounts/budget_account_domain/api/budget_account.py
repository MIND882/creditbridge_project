"""HTTP surface for Budget Account -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.budget_account_domain.schemas.budget_account import (

    BudgetAccountListResponse,

    BudgetAccountRead,

)

from app.accounts.budget_account_domain.services.budget_account_service import BudgetAccountService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = BudgetAccountService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=BudgetAccountListResponse, summary="List budget account rows")

def list_budget_account(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> BudgetAccountListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return BudgetAccountListResponse.from_result(

        page, [BudgetAccountRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=BudgetAccountRead, summary="Get one budget account row")

def get_budget_account(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> BudgetAccountRead:

    try:

        return BudgetAccountRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
