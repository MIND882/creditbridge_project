"""Data access for WorkstationType. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_type_domain.models.workstation_type import WorkstationType

from app.core.pagination import normalise_paging



__all__ = ["WorkstationTypeRepository"]





class WorkstationTypeRepository:

    model = WorkstationType





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkstationType]:

        return db.scalar(

            select(WorkstationType).where(

                WorkstationType.business_id == business_id, WorkstationType.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkstationType]:

        return db.scalar(

            select(WorkstationType).where(

                WorkstationType.business_id == business_id, WorkstationType.name == name

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

    ) -> tuple[Sequence[WorkstationType], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkstationType.business_id == business_id]

        if search:

            conditions.append(WorkstationType.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(WorkstationType).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkstationType)

            .where(*conditions)

            .order_by(WorkstationType.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: WorkstationType) -> WorkstationType:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: WorkstationType) -> None:

        db.delete(row)

        db.flush()
