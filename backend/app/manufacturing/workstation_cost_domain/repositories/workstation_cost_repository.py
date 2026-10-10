"""Data access for WorkstationCost. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_cost_domain.models.workstation_cost import WorkstationCost

from app.core.pagination import normalise_paging



__all__ = ["WorkstationCostRepository"]





class WorkstationCostRepository:

    model = WorkstationCost





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkstationCost]:

        return db.scalar(

            select(WorkstationCost).where(

                WorkstationCost.business_id == business_id, WorkstationCost.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkstationCost]:

        return db.scalar(

            select(WorkstationCost).where(

                WorkstationCost.business_id == business_id, WorkstationCost.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkstationCost], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkstationCost.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkstationCost.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkstationCost).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkstationCost)

            .where(*conditions)

            .order_by(WorkstationCost.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
