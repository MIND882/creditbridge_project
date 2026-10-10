"""Data access for POSItemGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_item_group_domain.models.pos_item_group import POSItemGroup

from app.core.pagination import normalise_paging



__all__ = ["POSItemGroupRepository"]





class POSItemGroupRepository:

    model = POSItemGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSItemGroup]:

        return db.scalar(

            select(POSItemGroup).where(

                POSItemGroup.business_id == business_id, POSItemGroup.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[POSItemGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSItemGroup.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSItemGroup.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSItemGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSItemGroup)

            .where(*conditions)

            .order_by(POSItemGroup.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


