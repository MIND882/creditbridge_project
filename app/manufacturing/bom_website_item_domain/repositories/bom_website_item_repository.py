"""Data access for BomWebsiteItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_website_item_domain.models.bom_website_item import BomWebsiteItem

from app.core.pagination import normalise_paging



__all__ = ["BomWebsiteItemRepository"]





class BomWebsiteItemRepository:

    model = BomWebsiteItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomWebsiteItem]:

        return db.scalar(

            select(BomWebsiteItem).where(

                BomWebsiteItem.business_id == business_id, BomWebsiteItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[BomWebsiteItem]:

        return db.scalar(

            select(BomWebsiteItem).where(

                BomWebsiteItem.business_id == business_id, BomWebsiteItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomWebsiteItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomWebsiteItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomWebsiteItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomWebsiteItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomWebsiteItem)

            .where(*conditions)

            .order_by(BomWebsiteItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
