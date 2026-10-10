"""Data access for PackedItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.packed_item_domain.models.packed_item import PackedItem

from app.core.pagination import normalise_paging



__all__ = ["PackedItemRepository"]





class PackedItemRepository:

    model = PackedItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PackedItem]:

        return db.scalar(

            select(PackedItem).where(

                PackedItem.business_id == business_id, PackedItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PackedItem]:

        return db.scalar(

            select(PackedItem).where(

                PackedItem.business_id == business_id, PackedItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PackedItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PackedItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(PackedItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PackedItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PackedItem)

            .where(*conditions)

            .order_by(PackedItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
