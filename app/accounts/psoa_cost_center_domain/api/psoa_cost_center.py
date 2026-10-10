"""HTTP surface for Psoa Cost Center -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.psoa_cost_center_domain.schemas.psoa_cost_center import (

    PsoaCostCenterListResponse,

    PsoaCostCenterRead,

)

from app.accounts.psoa_cost_center_domain.services.psoa_cost_center_service import PsoaCostCenterService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PsoaCostCenterService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PsoaCostCenterListResponse, summary="List psoa cost center rows")

def list_psoa_cost_center(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PsoaCostCenterListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PsoaCostCenterListResponse.from_result(

        page, [PsoaCostCenterRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PsoaCostCenterRead, summary="Get one psoa cost center row")

def get_psoa_cost_center(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PsoaCostCenterRead:

    try:

        return PsoaCostCenterRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
