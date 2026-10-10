"""Data access for ItemTax. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_tax_domain.models.item_tax import ItemTax

from app.core.pagination import normalise_paging



__all__ = ["ItemTaxRepository"]





class ItemTaxRepository:

    model = ItemTax





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemTax]:

        return db.scalar(

            select(ItemTax).where(

                ItemTax.business_id == business_id, ItemTax.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemTax]:

        return db.scalar(

            select(ItemTax).where(

                ItemTax.business_id == business_id, ItemTax.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemTax], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemTax.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemTax.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemTax).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemTax)

            .where(*conditions)

            .order_by(ItemTax.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
