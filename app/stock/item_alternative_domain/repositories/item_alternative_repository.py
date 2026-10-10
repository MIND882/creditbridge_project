"""Data access for ItemAlternative. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_alternative_domain.models.item_alternative import ItemAlternative

from app.core.pagination import normalise_paging



__all__ = ["ItemAlternativeRepository"]





class ItemAlternativeRepository:

    model = ItemAlternative





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemAlternative]:

        return db.scalar(

            select(ItemAlternative).where(

                ItemAlternative.business_id == business_id, ItemAlternative.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemAlternative]:

        return db.scalar(

            select(ItemAlternative).where(

                ItemAlternative.business_id == business_id, ItemAlternative.name == name

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

    ) -> tuple[Sequence[ItemAlternative], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemAlternative.business_id == business_id]

        if search:

            conditions.append(ItemAlternative.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemAlternative).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemAlternative)

            .where(*conditions)

            .order_by(ItemAlternative.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemAlternative) -> ItemAlternative:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemAlternative) -> None:

        db.delete(row)

        db.flush()
