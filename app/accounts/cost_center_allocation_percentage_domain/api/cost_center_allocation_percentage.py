"""

HTTP surface for Cost Center Allocation Percentage.



Read-only by design. This is a Frappe child table (``istable: 1``): rows are

created and edited through the parent Cost Center Allocation endpoints, which

own the ``idx`` ordering and the "percentages must total 100" invariant.

Exposing writes here would let a client break that invariant behind the parent

service's back.

"""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.cost_center_allocation_percentage_domain.schemas.cost_center_allocation_percentage import (

    CostCenterAllocationPercentageListResponse,

    CostCenterAllocationPercentageRead,

)

from app.accounts.cost_center_allocation_percentage_domain.services.cost_center_allocation_percentage_service import (

    CostCenterAllocationPercentageService,

)

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()

_service = CostCenterAllocationPercentageService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





def _read(row: object) -> CostCenterAllocationPercentageRead:

    return CostCenterAllocationPercentageRead.model_validate(row)





@router.get("", response_model=CostCenterAllocationPercentageListResponse, summary="List rows")

def list_rows(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

    cost_center_id: Optional[uuid.UUID] = Query(default=None),

) -> CostCenterAllocationPercentageListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit,

        parent_id=parent_id, cost_center_id=cost_center_id,

    )

    return CostCenterAllocationPercentageListResponse.from_result(

        page, [_read(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=CostCenterAllocationPercentageRead, summary="Get one row")

def get_row(row_id: uuid.UUID, db: DbDep, business_id: BusinessDep) -> CostCenterAllocationPercentageRead:

    try:

        return _read(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
