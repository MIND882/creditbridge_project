"""Data access for BomItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_item_domain.models.bom_item import BomItem

from app.core.pagination import normalise_paging



__all__ = ["BomItemRepository"]





class BomItemRepository:

    model = BomItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomItem]:

        return db.scalar(

            select(BomItem).where(

                BomItem.business_id == business_id, BomItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomItem]:

        return db.scalar(

            select(BomItem).where(

                BomItem.business_id == business_id, BomItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomItem)

            .where(*conditions)

            .order_by(BomItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
