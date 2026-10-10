"""Data access for WorkOrderOperation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.work_order_operation_domain.models.work_order_operation import WorkOrderOperation

from app.core.pagination import normalise_paging



__all__ = ["WorkOrderOperationRepository"]





class WorkOrderOperationRepository:

    model = WorkOrderOperation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkOrderOperation]:

        return db.scalar(

            select(WorkOrderOperation).where(

                WorkOrderOperation.business_id == business_id, WorkOrderOperation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkOrderOperation]:

        return db.scalar(

            select(WorkOrderOperation).where(

                WorkOrderOperation.business_id == business_id, WorkOrderOperation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkOrderOperation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkOrderOperation.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkOrderOperation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkOrderOperation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkOrderOperation)

            .where(*conditions)

            .order_by(WorkOrderOperation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
