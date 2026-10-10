"""Data access for PackingSlipItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.packing_slip_item_domain.models.packing_slip_item import PackingSlipItem

from app.core.pagination import normalise_paging



__all__ = ["PackingSlipItemRepository"]





class PackingSlipItemRepository:

    model = PackingSlipItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PackingSlipItem]:

        return db.scalar(

            select(PackingSlipItem).where(

                PackingSlipItem.business_id == business_id, PackingSlipItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PackingSlipItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PackingSlipItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(PackingSlipItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PackingSlipItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PackingSlipItem)

            .where(*conditions)

            .order_by(PackingSlipItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
