"""Data access for BomCreatorItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_creator_item_domain.models.bom_creator_item import BomCreatorItem

from app.core.pagination import normalise_paging



__all__ = ["BomCreatorItemRepository"]





class BomCreatorItemRepository:

    model = BomCreatorItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomCreatorItem]:

        return db.scalar(

            select(BomCreatorItem).where(

                BomCreatorItem.business_id == business_id, BomCreatorItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomCreatorItem]:

        return db.scalar(

            select(BomCreatorItem).where(

                BomCreatorItem.business_id == business_id, BomCreatorItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomCreatorItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomCreatorItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomCreatorItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomCreatorItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomCreatorItem)

            .where(*conditions)

            .order_by(BomCreatorItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
