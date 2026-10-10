"""HTTP surface for Production Plan Item Reference -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_item_reference_domain.schemas.production_plan_item_reference import (

    ProductionPlanItemReferenceListResponse,

    ProductionPlanItemReferenceRead,

)

from app.manufacturing.production_plan_item_reference_domain.services.production_plan_item_reference_service import ProductionPlanItemReferenceService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ProductionPlanItemReferenceService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ProductionPlanItemReferenceListResponse, summary="List production plan item reference rows")

def list_production_plan_item_reference(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ProductionPlanItemReferenceListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ProductionPlanItemReferenceListResponse.from_result(

        page, [ProductionPlanItemReferenceRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ProductionPlanItemReferenceRead, summary="Get one production plan item reference row"

)

def get_production_plan_item_reference(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ProductionPlanItemReferenceRead:

    try:

        return ProductionPlanItemReferenceRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
