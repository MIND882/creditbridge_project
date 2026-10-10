"""Data access for WorkOrderAdditionalItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.core.pagination import normalise_paging



__all__ = ["WorkOrderAdditionalItemRepository"]





class WorkOrderAdditionalItemRepository:

    model = WorkOrderAdditionalItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkOrderAdditionalItem]:

        return db.scalar(

            select(WorkOrderAdditionalItem).where(

                WorkOrderAdditionalItem.business_id == business_id, WorkOrderAdditionalItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkOrderAdditionalItem]:

        return db.scalar(

            select(WorkOrderAdditionalItem).where(

                WorkOrderAdditionalItem.business_id == business_id, WorkOrderAdditionalItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkOrderAdditionalItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkOrderAdditionalItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkOrderAdditionalItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkOrderAdditionalItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkOrderAdditionalItem)

            .where(*conditions)

            .order_by(WorkOrderAdditionalItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
