"""Data access for TerritoryItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.territory_item_domain.models.territory_item import TerritoryItem

from app.core.pagination import normalise_paging



__all__ = ["TerritoryItemRepository"]





class TerritoryItemRepository:

    model = TerritoryItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[TerritoryItem]:

        return db.scalar(

            select(TerritoryItem).where(

                TerritoryItem.business_id == business_id, TerritoryItem.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[TerritoryItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TerritoryItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(TerritoryItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(TerritoryItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(TerritoryItem)

            .where(*conditions)

            .order_by(TerritoryItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


