"""Data access for ItemVariant. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_variant_domain.models.item_variant import ItemVariant

from app.core.pagination import normalise_paging



__all__ = ["ItemVariantRepository"]





class ItemVariantRepository:

    model = ItemVariant





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemVariant]:

        return db.scalar(

            select(ItemVariant).where(

                ItemVariant.business_id == business_id, ItemVariant.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemVariant]:

        return db.scalar(

            select(ItemVariant).where(

                ItemVariant.business_id == business_id, ItemVariant.name == name

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

    ) -> tuple[Sequence[ItemVariant], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemVariant.business_id == business_id]

        if search:

            conditions.append(ItemVariant.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemVariant).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemVariant)

            .where(*conditions)

            .order_by(ItemVariant.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemVariant) -> ItemVariant:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemVariant) -> None:

        db.delete(row)

        db.flush()
