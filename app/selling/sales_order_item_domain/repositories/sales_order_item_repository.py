"""Data access for SalesOrderItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sales_order_item_domain.models.sales_order_item import SalesOrderItem

from app.core.pagination import normalise_paging



__all__ = ["SalesOrderItemRepository"]





class SalesOrderItemRepository:

    model = SalesOrderItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesOrderItem]:

        return db.scalar(

            select(SalesOrderItem).where(

                SalesOrderItem.business_id == business_id, SalesOrderItem.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SalesOrderItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesOrderItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesOrderItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesOrderItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesOrderItem)

            .where(*conditions)

            .order_by(SalesOrderItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
