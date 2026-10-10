"""Data access for ShipmentParcelTemplate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.shipment_parcel_template_domain.models.shipment_parcel_template import ShipmentParcelTemplate

from app.core.pagination import normalise_paging



__all__ = ["ShipmentParcelTemplateRepository"]





class ShipmentParcelTemplateRepository:

    model = ShipmentParcelTemplate





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShipmentParcelTemplate]:

        return db.scalar(

            select(ShipmentParcelTemplate).where(

                ShipmentParcelTemplate.business_id == business_id, ShipmentParcelTemplate.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShipmentParcelTemplate]:

        return db.scalar(

            select(ShipmentParcelTemplate).where(

                ShipmentParcelTemplate.business_id == business_id, ShipmentParcelTemplate.name == name

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

    ) -> tuple[Sequence[ShipmentParcelTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShipmentParcelTemplate.business_id == business_id]

        if search:

            conditions.append(ShipmentParcelTemplate.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ShipmentParcelTemplate).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShipmentParcelTemplate)

            .where(*conditions)

            .order_by(ShipmentParcelTemplate.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ShipmentParcelTemplate) -> ShipmentParcelTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ShipmentParcelTemplate) -> None:

        db.delete(row)

        db.flush()
