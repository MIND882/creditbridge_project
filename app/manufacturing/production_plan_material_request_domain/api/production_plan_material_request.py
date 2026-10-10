"""HTTP surface for Production Plan Material Request -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.manufacturing.production_plan_material_request_domain.schemas.production_plan_material_request import (

    ProductionPlanMaterialRequestListResponse,

    ProductionPlanMaterialRequestRead,

)

from app.manufacturing.production_plan_material_request_domain.services.production_plan_material_request_service import ProductionPlanMaterialRequestService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ProductionPlanMaterialRequestService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ProductionPlanMaterialRequestListResponse, summary="List production plan material request rows")

def list_production_plan_material_request(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ProductionPlanMaterialRequestListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ProductionPlanMaterialRequestListResponse.from_result(

        page, [ProductionPlanMaterialRequestRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ProductionPlanMaterialRequestRead, summary="Get one production plan material request row"

)

def get_production_plan_material_request(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ProductionPlanMaterialRequestRead:

    try:

        return ProductionPlanMaterialRequestRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
