"""Data access for DeliveryStop. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_stop_domain.models.delivery_stop import DeliveryStop

from app.core.pagination import normalise_paging



__all__ = ["DeliveryStopRepository"]





class DeliveryStopRepository:

    model = DeliveryStop





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DeliveryStop]:

        return db.scalar(

            select(DeliveryStop).where(

                DeliveryStop.business_id == business_id, DeliveryStop.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DeliveryStop]:

        return db.scalar(

            select(DeliveryStop).where(

                DeliveryStop.business_id == business_id, DeliveryStop.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[DeliveryStop], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DeliveryStop.business_id == business_id]

        if parent_id is not None:

            conditions.append(DeliveryStop.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(DeliveryStop).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DeliveryStop)

            .where(*conditions)

            .order_by(DeliveryStop.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
