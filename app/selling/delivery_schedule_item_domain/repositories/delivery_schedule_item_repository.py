"""Data access for DeliveryScheduleItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.delivery_schedule_item_domain.models.delivery_schedule_item import DeliveryScheduleItem

from app.core.pagination import normalise_paging



__all__ = ["DeliveryScheduleItemRepository"]





class DeliveryScheduleItemRepository:

    model = DeliveryScheduleItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[DeliveryScheduleItem]:

        return db.scalar(

            select(DeliveryScheduleItem).where(

                DeliveryScheduleItem.business_id == business_id, DeliveryScheduleItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[DeliveryScheduleItem]:

        return db.scalar(

            select(DeliveryScheduleItem).where(

                DeliveryScheduleItem.business_id == business_id, DeliveryScheduleItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[DeliveryScheduleItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [DeliveryScheduleItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(DeliveryScheduleItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(DeliveryScheduleItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(DeliveryScheduleItem)

            .where(*conditions)

            .order_by(DeliveryScheduleItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
