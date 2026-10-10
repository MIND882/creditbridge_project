"""Data access for ItemReorder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_reorder_domain.models.item_reorder import ItemReorder

from app.core.pagination import normalise_paging



__all__ = ["ItemReorderRepository"]





class ItemReorderRepository:

    model = ItemReorder





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemReorder]:

        return db.scalar(

            select(ItemReorder).where(

                ItemReorder.business_id == business_id, ItemReorder.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemReorder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemReorder.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemReorder.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemReorder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemReorder)

            .where(*conditions)

            .order_by(ItemReorder.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
