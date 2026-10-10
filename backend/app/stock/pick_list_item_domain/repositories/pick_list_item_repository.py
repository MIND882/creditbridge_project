"""Data access for PickListItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.pick_list_item_domain.models.pick_list_item import PickListItem

from app.core.pagination import normalise_paging



__all__ = ["PickListItemRepository"]





class PickListItemRepository:

    model = PickListItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PickListItem]:

        return db.scalar(

            select(PickListItem).where(

                PickListItem.business_id == business_id, PickListItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PickListItem]:

        return db.scalar(

            select(PickListItem).where(

                PickListItem.business_id == business_id, PickListItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PickListItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PickListItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(PickListItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PickListItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PickListItem)

            .where(*conditions)

            .order_by(PickListItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
