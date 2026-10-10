"""Business logic for ShipmentDeliveryNote.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.shipment_delivery_note_domain.models.shipment_delivery_note import ShipmentDeliveryNote

from app.stock.shipment_delivery_note_domain.repositories.shipment_delivery_note_repository import (

    ShipmentDeliveryNoteRepository,

)

from app.stock.shipment_delivery_note_domain.schemas.shipment_delivery_note import (

    ShipmentDeliveryNoteCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShipmentDeliveryNoteService"]





class ShipmentDeliveryNoteService:

    def __init__(self, repository: Optional[ShipmentDeliveryNoteRepository] = None) -> None:

        self.repository = repository or ShipmentDeliveryNoteRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShipmentDeliveryNote:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipment Delivery Note", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShipmentDeliveryNote]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShipmentDeliveryNote].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
