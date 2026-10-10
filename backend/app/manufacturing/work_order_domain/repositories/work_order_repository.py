"""Data access for WorkOrder. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.work_order_domain.models.work_order import WorkOrder

from app.core.pagination import normalise_paging



__all__ = ["WorkOrderRepository"]





class WorkOrderRepository:

    model = WorkOrder





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkOrder]:

        return db.scalar(

            select(WorkOrder).where(

                WorkOrder.business_id == business_id, WorkOrder.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkOrder]:

        return db.scalar(

            select(WorkOrder).where(

                WorkOrder.business_id == business_id, WorkOrder.name == name

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

    ) -> tuple[Sequence[WorkOrder], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkOrder.business_id == business_id]

        if not include_cancelled:

            conditions.append(WorkOrder.docstatus != 2)

        if search:

            conditions.append(WorkOrder.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(WorkOrder).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkOrder)

            .where(*conditions)

            .order_by(WorkOrder.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: WorkOrder) -> WorkOrder:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: WorkOrder) -> None:

        db.delete(row)

        db.flush()
