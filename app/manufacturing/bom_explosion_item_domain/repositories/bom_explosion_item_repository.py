"""Data access for BomExplosionItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_explosion_item_domain.models.bom_explosion_item import BomExplosionItem

from app.core.pagination import normalise_paging



__all__ = ["BomExplosionItemRepository"]





class BomExplosionItemRepository:

    model = BomExplosionItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomExplosionItem]:

        return db.scalar(

            select(BomExplosionItem).where(

                BomExplosionItem.business_id == business_id, BomExplosionItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomExplosionItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomExplosionItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomExplosionItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomExplosionItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomExplosionItem)

            .where(*conditions)

            .order_by(BomExplosionItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
