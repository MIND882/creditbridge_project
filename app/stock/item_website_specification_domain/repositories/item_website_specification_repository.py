"""Data access for ItemWebsiteSpecification. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_website_specification_domain.models.item_website_specification import ItemWebsiteSpecification

from app.core.pagination import normalise_paging



__all__ = ["ItemWebsiteSpecificationRepository"]





class ItemWebsiteSpecificationRepository:

    model = ItemWebsiteSpecification





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemWebsiteSpecification]:

        return db.scalar(

            select(ItemWebsiteSpecification).where(

                ItemWebsiteSpecification.business_id == business_id, ItemWebsiteSpecification.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ItemWebsiteSpecification]:

        return db.scalar(

            select(ItemWebsiteSpecification).where(

                ItemWebsiteSpecification.business_id == business_id, ItemWebsiteSpecification.name == name

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

    ) -> tuple[Sequence[ItemWebsiteSpecification], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemWebsiteSpecification.business_id == business_id]

        if search:

            conditions.append(ItemWebsiteSpecification.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ItemWebsiteSpecification).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemWebsiteSpecification)

            .where(*conditions)

            .order_by(ItemWebsiteSpecification.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ItemWebsiteSpecification) -> ItemWebsiteSpecification:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ItemWebsiteSpecification) -> None:

        db.delete(row)

        db.flush()
