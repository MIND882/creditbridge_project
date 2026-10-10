"""Data access for Item. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_domain.models.item import Item

from app.core.pagination import normalise_paging



__all__ = ["ItemRepository"]





class ItemRepository:

    model = Item





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Item]:

        return db.scalar(

            select(Item).where(

                Item.business_id == business_id, Item.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Item]:

        return db.scalar(

            select(Item).where(

                Item.business_id == business_id, Item.name == name

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

    ) -> tuple[Sequence[Item], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Item.business_id == business_id]

        if search:

            conditions.append(Item.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Item).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Item)

            .where(*conditions)

            .order_by(Item.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Item) -> Item:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Item) -> None:

        db.delete(row)

        db.flush()
