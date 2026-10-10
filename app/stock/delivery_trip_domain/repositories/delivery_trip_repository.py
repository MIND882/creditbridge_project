"""Data access for DeliveryTrip. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_trip_domain.models.delivery_trip import DeliveryTrip

from app.core.pagination import normalise_paging



__all__ = ["DeliveryTripRepository"]





class DeliveryTripRepository:

    model = DeliveryTrip





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DeliveryTrip]:

        return db.scalar(

            select(DeliveryTrip).where(

                DeliveryTrip.business_id == business_id, DeliveryTrip.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DeliveryTrip]:

        return db.scalar(

            select(DeliveryTrip).where(

                DeliveryTrip.business_id == business_id, DeliveryTrip.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[DeliveryTrip], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DeliveryTrip.business_id == business_id]

        if not include_cancelled:

            conditions.append(DeliveryTrip.docstatus != 2)

        if search:

            conditions.append(DeliveryTrip.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(DeliveryTrip).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DeliveryTrip)

            .where(*conditions)

            .order_by(DeliveryTrip.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: DeliveryTrip) -> DeliveryTrip:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: DeliveryTrip) -> None:

        db.delete(row)

        db.flush()
