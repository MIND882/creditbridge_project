"""HTTP surface for Shipment Parcel -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.shipment_parcel_domain.schemas.shipment_parcel import (

    ShipmentParcelListResponse,

    ShipmentParcelRead,

)

from app.stock.shipment_parcel_domain.services.shipment_parcel_service import ShipmentParcelService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ShipmentParcelService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ShipmentParcelListResponse, summary="List shipment parcel rows")

def list_shipment_parcel(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ShipmentParcelListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ShipmentParcelListResponse.from_result(

        page, [ShipmentParcelRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ShipmentParcelRead, summary="Get one shipment parcel row"

)

def get_shipment_parcel(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ShipmentParcelRead:

    try:

        return ShipmentParcelRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
