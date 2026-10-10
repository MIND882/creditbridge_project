"""Data access for WorkstationWorkingHour. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_working_hour_domain.models.workstation_working_hour import WorkstationWorkingHour

from app.core.pagination import normalise_paging



__all__ = ["WorkstationWorkingHourRepository"]





class WorkstationWorkingHourRepository:

    model = WorkstationWorkingHour





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkstationWorkingHour]:

        return db.scalar(

            select(WorkstationWorkingHour).where(

                WorkstationWorkingHour.business_id == business_id, WorkstationWorkingHour.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkstationWorkingHour]:

        return db.scalar(

            select(WorkstationWorkingHour).where(

                WorkstationWorkingHour.business_id == business_id, WorkstationWorkingHour.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkstationWorkingHour], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkstationWorkingHour.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkstationWorkingHour.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkstationWorkingHour).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkstationWorkingHour)

            .where(*conditions)

            .order_by(WorkstationWorkingHour.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
