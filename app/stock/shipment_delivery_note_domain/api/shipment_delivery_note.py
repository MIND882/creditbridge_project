"""HTTP surface for Shipment Delivery Note -- read-only child table."""



from __future__ import annotations



import uuid

from typing import Annotated, Optional



from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session



from app.stock.shipment_delivery_note_domain.schemas.shipment_delivery_note import (

    ShipmentDeliveryNoteListResponse,

    ShipmentDeliveryNoteRead,

)

from app.stock.shipment_delivery_note_domain.services.shipment_delivery_note_service import ShipmentDeliveryNoteService

from app.core.errors import NotFoundError

from app.core.pagination import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

from app.core.tenancy import get_current_business_uuid, get_db



__all__ = ["router"]



router = APIRouter()



_service = ShipmentDeliveryNoteService()



DbDep = Annotated[Session, Depends(get_db)]

BusinessDep = Annotated[uuid.UUID, Depends(get_current_business_uuid)]





@router.get("", response_model=ShipmentDeliveryNoteListResponse, summary="List shipment delivery note rows")

def list_shipment_delivery_note(

    db: DbDep,

    business_id: BusinessDep,

    offset: Annotated[int, Query(ge=0)] = 0,

    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,

    parent_id: Optional[uuid.UUID] = Query(default=None),

) -> ShipmentDeliveryNoteListResponse:

    page = _service.list(

        db, business_id, offset=offset, limit=limit, parent_id=parent_id

    )

    return ShipmentDeliveryNoteListResponse.from_result(

        page, [ShipmentDeliveryNoteRead.model_validate(r) for r in page.items]

    )





@router.get(

    "/{row_id}", response_model=ShipmentDeliveryNoteRead, summary="Get one shipment delivery note row"

)

def get_shipment_delivery_note(

    row_id: uuid.UUID, db: DbDep, business_id: BusinessDep

) -> ShipmentDeliveryNoteRead:

    try:

        return ShipmentDeliveryNoteRead.model_validate(_service.get(db, business_id, row_id))

    except NotFoundError as exc:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)

        ) from exc
