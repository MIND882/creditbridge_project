"""Data access for BomSecondaryItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item import BomSecondaryItem

from app.core.pagination import normalise_paging



__all__ = ["BomSecondaryItemRepository"]





class BomSecondaryItemRepository:

    model = BomSecondaryItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomSecondaryItem]:

        return db.scalar(

            select(BomSecondaryItem).where(

                BomSecondaryItem.business_id == business_id, BomSecondaryItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomSecondaryItem]:

        return db.scalar(

            select(BomSecondaryItem).where(

                BomSecondaryItem.business_id == business_id, BomSecondaryItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomSecondaryItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomSecondaryItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomSecondaryItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomSecondaryItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomSecondaryItem)

            .where(*conditions)

            .order_by(BomSecondaryItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
