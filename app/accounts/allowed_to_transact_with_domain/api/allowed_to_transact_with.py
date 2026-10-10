"""HTTP surface for Allowed To Transact With -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.allowed_to_transact_with_domain.schemas.allowed_to_transact_with import (

    AllowedToTransactWithListResponse,

    AllowedToTransactWithRead,

)

from app.accounts.allowed_to_transact_with_domain.services.allowed_to_transact_with_service import AllowedToTransactWithService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = AllowedToTransactWithService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=AllowedToTransactWithListResponse, summary="List allowed to transact with rows")

def list_allowed_to_transact_with(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> AllowedToTransactWithListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return AllowedToTransactWithListResponse.from_result(

        page, [AllowedToTransactWithRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=AllowedToTransactWithRead, summary="Get one allowed to transact with row")

def get_allowed_to_transact_with(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> AllowedToTransactWithRead:

    try:

        return AllowedToTransactWithRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
