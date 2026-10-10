"""Data access for ItemLeadTime. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_lead_time_domain.models.item_lead_time import ItemLeadTime

from app.core.pagination import normalise_paging



__all__ = ["ItemLeadTimeRepository"]





class ItemLeadTimeRepository:

    model = ItemLeadTime





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemLeadTime]:

        return db.scalar(

            select(ItemLeadTime).where(

                ItemLeadTime.business_id == business_id, ItemLeadTime.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemLeadTime]:

        return db.scalar(

            select(ItemLeadTime).where(

                ItemLeadTime.business_id == business_id, ItemLeadTime.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[ItemLeadTime], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemLeadTime.business_id == business_id]

        if search:

            conditions.append(ItemLeadTime.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemLeadTime).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemLeadTime)

            .where(*conditions)

            .order_by(ItemLeadTime.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemLeadTime) -> ItemLeadTime:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemLeadTime) -> None:

        db.delete(row)

        db.flush()
