"""HTTP surface for POS Item Group -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.accounts.pos_item_group_domain.schemas.pos_item_group import (

    POSItemGroupListResponse,

    POSItemGroupRead,

)

from app.accounts.pos_item_group_domain.services.pos_item_group_service import POSItemGroupService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = POSItemGroupService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=POSItemGroupListResponse, summary="List pos item group rows")

def list_pos_item_group(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> POSItemGroupListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return POSItemGroupListResponse.from_result(

        page, [POSItemGroupRead.model_validate(r) for r in page.items]

    )





@router.get("/{row_id}", response_model=POSItemGroupRead, summary="Get one pos item group row")

def get_pos_item_group(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> POSItemGroupRead:

    try:

        return POSItemGroupRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
