"""Data access for LandedCostItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.landed_cost_item_domain.models.landed_cost_item import LandedCostItem

from app.core.pagination import normalise_paging



__all__ = ["LandedCostItemRepository"]





class LandedCostItemRepository:

    model = LandedCostItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[LandedCostItem]:

        return db.scalar(

            select(LandedCostItem).where(

                LandedCostItem.business_id == business_id, LandedCostItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[LandedCostItem]:

        return db.scalar(

            select(LandedCostItem).where(

                LandedCostItem.business_id == business_id, LandedCostItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[LandedCostItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [LandedCostItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(LandedCostItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(LandedCostItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(LandedCostItem)

            .where(*conditions)

            .order_by(LandedCostItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
