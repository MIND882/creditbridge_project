"""HTTP surface for Psoa Project -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.psoa_project_domain.schemas.psoa_project import (

    PsoaProjectListResponse,

    PsoaProjectRead,

)

from app.accounts.psoa_project_domain.services.psoa_project_service import PsoaProjectService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = PsoaProjectService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=PsoaProjectListResponse, summary="List psoa project rows")

def list_psoa_project(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> PsoaProjectListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return PsoaProjectListResponse.from_result(

        page, [PsoaProjectRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=PsoaProjectRead, summary="Get one psoa project row")

def get_psoa_project(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> PsoaProjectRead:

    try:

        return PsoaProjectRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
