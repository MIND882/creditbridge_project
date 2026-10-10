"""Data access for ItemDefault. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_default_domain.models.item_default import ItemDefault

from app.core.pagination import normalise_paging



__all__ = ["ItemDefaultRepository"]





class ItemDefaultRepository:

    model = ItemDefault





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemDefault]:

        return db.scalar(

            select(ItemDefault).where(

                ItemDefault.business_id == business_id, ItemDefault.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemDefault]:

        return db.scalar(

            select(ItemDefault).where(

                ItemDefault.business_id == business_id, ItemDefault.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemDefault], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemDefault.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemDefault.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemDefault).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemDefault)

            .where(*conditions)

            .order_by(ItemDefault.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
