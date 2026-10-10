"""Data access for ItemPrice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_price_domain.models.item_price import ItemPrice

from app.core.pagination import normalise_paging



__all__ = ["ItemPriceRepository"]





class ItemPriceRepository:

    model = ItemPrice





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemPrice]:

        return db.scalar(

            select(ItemPrice).where(

                ItemPrice.business_id == business_id, ItemPrice.id == row_id

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

    ) -> tuple[Sequence[ItemPrice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemPrice.business_id == business_id]

        if search:

            conditions.append(ItemPrice.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemPrice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemPrice)

            .where(*conditions)

            .order_by(ItemPrice.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemPrice) -> ItemPrice:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemPrice) -> None:

        db.delete(row)

        db.flush()
