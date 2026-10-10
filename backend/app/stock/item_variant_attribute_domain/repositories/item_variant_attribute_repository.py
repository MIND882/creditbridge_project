"""Data access for ItemVariantAttribute. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_variant_attribute_domain.models.item_variant_attribute import ItemVariantAttribute

from app.core.pagination import normalise_paging



__all__ = ["ItemVariantAttributeRepository"]





class ItemVariantAttributeRepository:

    model = ItemVariantAttribute





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemVariantAttribute]:

        return db.scalar(

            select(ItemVariantAttribute).where(

                ItemVariantAttribute.business_id == business_id, ItemVariantAttribute.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemVariantAttribute]:

        return db.scalar(

            select(ItemVariantAttribute).where(

                ItemVariantAttribute.business_id == business_id, ItemVariantAttribute.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemVariantAttribute], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemVariantAttribute.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemVariantAttribute.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemVariantAttribute).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemVariantAttribute)

            .where(*conditions)

            .order_by(ItemVariantAttribute.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
