"""Data access for ItemGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_group_domain.models.item_group import ItemGroup

from app.core.pagination import normalise_paging



__all__ = ["ItemGroupRepository"]





class ItemGroupRepository:

    model = ItemGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemGroup]:

        return db.scalar(

            select(ItemGroup).where(

                ItemGroup.business_id == business_id, ItemGroup.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemGroup]:

        return db.scalar(

            select(ItemGroup).where(

                ItemGroup.business_id == business_id, ItemGroup.name == name

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

    ) -> tuple[Sequence[ItemGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemGroup.business_id == business_id]

        if search:

            conditions.append(ItemGroup.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemGroup)

            .where(*conditions)

            .order_by(ItemGroup.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemGroup) -> ItemGroup:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemGroup) -> None:

        db.delete(row)

        db.flush()
