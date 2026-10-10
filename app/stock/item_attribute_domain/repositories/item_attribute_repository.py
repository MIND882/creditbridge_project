"""Data access for ItemAttribute. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_attribute_domain.models.item_attribute import ItemAttribute

from app.core.pagination import normalise_paging



__all__ = ["ItemAttributeRepository"]





class ItemAttributeRepository:

    model = ItemAttribute





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemAttribute]:

        return db.scalar(

            select(ItemAttribute).where(

                ItemAttribute.business_id == business_id, ItemAttribute.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemAttribute]:

        return db.scalar(

            select(ItemAttribute).where(

                ItemAttribute.business_id == business_id, ItemAttribute.name == name

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

    ) -> tuple[Sequence[ItemAttribute], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemAttribute.business_id == business_id]

        if search:

            conditions.append(ItemAttribute.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemAttribute).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemAttribute)

            .where(*conditions)

            .order_by(ItemAttribute.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemAttribute) -> ItemAttribute:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemAttribute) -> None:

        db.delete(row)

        db.flush()
