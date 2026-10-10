"""HTTP surface for Workstation Cost -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.workstation_cost_domain.schemas.workstation_cost import (

    WorkstationCostListResponse,

    WorkstationCostRead,

)

from app.manufacturing.workstation_cost_domain.services.workstation_cost_service import WorkstationCostService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = WorkstationCostService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=WorkstationCostListResponse, summary="List workstation cost rows")

def list_workstation_cost(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> WorkstationCostListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return WorkstationCostListResponse.from_result(

        page, [WorkstationCostRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=WorkstationCostRead, summary="Get one workstation cost row"

)

def get_workstation_cost(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> WorkstationCostRead:

    try:

        return WorkstationCostRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
