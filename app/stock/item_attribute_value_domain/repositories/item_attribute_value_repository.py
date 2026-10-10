"""Data access for ItemAttributeValue. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_attribute_value_domain.models.item_attribute_value import ItemAttributeValue

from app.core.pagination import normalise_paging



__all__ = ["ItemAttributeValueRepository"]





class ItemAttributeValueRepository:

    model = ItemAttributeValue





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemAttributeValue]:

        return db.scalar(

            select(ItemAttributeValue).where(

                ItemAttributeValue.business_id == business_id, ItemAttributeValue.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemAttributeValue]:

        return db.scalar(

            select(ItemAttributeValue).where(

                ItemAttributeValue.business_id == business_id, ItemAttributeValue.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemAttributeValue], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemAttributeValue.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemAttributeValue.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemAttributeValue).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemAttributeValue)

            .where(*conditions)

            .order_by(ItemAttributeValue.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
