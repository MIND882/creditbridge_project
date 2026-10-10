"""HTTP surface for Workstation Working Hour -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.workstation_working_hour_domain.schemas.workstation_working_hour import (

    WorkstationWorkingHourListResponse,

    WorkstationWorkingHourRead,

)

from app.manufacturing.workstation_working_hour_domain.services.workstation_working_hour_service import WorkstationWorkingHourService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = WorkstationWorkingHourService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=WorkstationWorkingHourListResponse, summary="List workstation working hour rows")

def list_workstation_working_hour(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> WorkstationWorkingHourListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return WorkstationWorkingHourListResponse.from_result(

        page, [WorkstationWorkingHourRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=WorkstationWorkingHourRead, summary="Get one workstation working hour row"

)

def get_workstation_working_hour(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> WorkstationWorkingHourRead:

    try:

        return WorkstationWorkingHourRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
