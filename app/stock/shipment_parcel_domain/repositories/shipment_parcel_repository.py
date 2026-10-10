"""Data access for ShipmentParcel. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_parcel_domain.models.shipment_parcel import ShipmentParcel

from app.core.pagination import normalise_paging



__all__ = ["ShipmentParcelRepository"]





class ShipmentParcelRepository:

    model = ShipmentParcel





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShipmentParcel]:

        return db.scalar(

            select(ShipmentParcel).where(

                ShipmentParcel.business_id == business_id, ShipmentParcel.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShipmentParcel]:

        return db.scalar(

            select(ShipmentParcel).where(

                ShipmentParcel.business_id == business_id, ShipmentParcel.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ShipmentParcel], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShipmentParcel.business_id == business_id]

        if parent_id is not None:

            conditions.append(ShipmentParcel.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ShipmentParcel).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShipmentParcel)

            .where(*conditions)

            .order_by(ShipmentParcel.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
