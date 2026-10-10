"""Data access for ShipmentDeliveryNote. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_delivery_note_domain.models.shipment_delivery_note import ShipmentDeliveryNote

from app.core.pagination import normalise_paging



__all__ = ["ShipmentDeliveryNoteRepository"]





class ShipmentDeliveryNoteRepository:

    model = ShipmentDeliveryNote





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShipmentDeliveryNote]:

        return db.scalar(

            select(ShipmentDeliveryNote).where(

                ShipmentDeliveryNote.business_id == business_id, ShipmentDeliveryNote.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShipmentDeliveryNote]:

        return db.scalar(

            select(ShipmentDeliveryNote).where(

                ShipmentDeliveryNote.business_id == business_id, ShipmentDeliveryNote.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ShipmentDeliveryNote], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShipmentDeliveryNote.business_id == business_id]

        if parent_id is not None:

            conditions.append(ShipmentDeliveryNote.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ShipmentDeliveryNote).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShipmentDeliveryNote)

            .where(*conditions)

            .order_by(ShipmentDeliveryNote.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
