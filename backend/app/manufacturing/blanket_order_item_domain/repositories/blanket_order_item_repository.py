"""Data access for BlanketOrderItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.blanket_order_item_domain.models.blanket_order_item import BlanketOrderItem

from app.core.pagination import normalise_paging



__all__ = ["BlanketOrderItemRepository"]





class BlanketOrderItemRepository:

    model = BlanketOrderItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BlanketOrderItem]:

        return db.scalar(

            select(BlanketOrderItem).where(

                BlanketOrderItem.business_id == business_id, BlanketOrderItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BlanketOrderItem]:

        return db.scalar(

            select(BlanketOrderItem).where(

                BlanketOrderItem.business_id == business_id, BlanketOrderItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BlanketOrderItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BlanketOrderItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BlanketOrderItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BlanketOrderItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BlanketOrderItem)

            .where(*conditions)

            .order_by(BlanketOrderItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
