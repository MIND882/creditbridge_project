"""HTTP surface for Work Order Additional Item -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.work_order_additional_item_domain.schemas.work_order_additional_item import (

    WorkOrderAdditionalItemListResponse,

    WorkOrderAdditionalItemRead,

)

from app.manufacturing.work_order_additional_item_domain.services.work_order_additional_item_service import WorkOrderAdditionalItemService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = WorkOrderAdditionalItemService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=WorkOrderAdditionalItemListResponse, summary="List work order additional item rows")

def list_work_order_additional_item(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> WorkOrderAdditionalItemListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return WorkOrderAdditionalItemListResponse.from_result(

        page, [WorkOrderAdditionalItemRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=WorkOrderAdditionalItemRead, summary="Get one work order additional item row"

)

def get_work_order_additional_item(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> WorkOrderAdditionalItemRead:

    try:

        return WorkOrderAdditionalItemRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
