"""Data access for Shipment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_domain.models.shipment import Shipment

from app.core.pagination import normalise_paging



__all__ = ["ShipmentRepository"]





class ShipmentRepository:

    model = Shipment





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Shipment]:

        return db.scalar(

            select(Shipment).where(

                Shipment.business_id == business_id, Shipment.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Shipment]:

        return db.scalar(

            select(Shipment).where(

                Shipment.business_id == business_id, Shipment.name == name

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

    ) -> tuple[Sequence[Shipment], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Shipment.business_id == business_id]

        if not include_cancelled:

            conditions.append(Shipment.docstatus != 2)

        if search:

            conditions.append(Shipment.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Shipment).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Shipment)

            .where(*conditions)

            .order_by(Shipment.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Shipment) -> Shipment:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Shipment) -> None:

        db.delete(row)

        db.flush()
