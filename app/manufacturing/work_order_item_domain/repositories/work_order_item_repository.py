"""Data access for WorkOrderItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.work_order_item_domain.models.work_order_item import WorkOrderItem

from app.core.pagination import normalise_paging



__all__ = ["WorkOrderItemRepository"]





class WorkOrderItemRepository:

    model = WorkOrderItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkOrderItem]:

        return db.scalar(

            select(WorkOrderItem).where(

                WorkOrderItem.business_id == business_id, WorkOrderItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkOrderItem]:

        return db.scalar(

            select(WorkOrderItem).where(

                WorkOrderItem.business_id == business_id, WorkOrderItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkOrderItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkOrderItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkOrderItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkOrderItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkOrderItem)

            .where(*conditions)

            .order_by(WorkOrderItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
