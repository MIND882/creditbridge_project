"""Data access for WorkstationOperatingComponent. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_operating_component_domain.models.workstation_operating_component import WorkstationOperatingComponent

from app.core.pagination import normalise_paging



__all__ = ["WorkstationOperatingComponentRepository"]





class WorkstationOperatingComponentRepository:

    model = WorkstationOperatingComponent





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkstationOperatingComponent]:

        return db.scalar(

            select(WorkstationOperatingComponent).where(

                WorkstationOperatingComponent.business_id == business_id, WorkstationOperatingComponent.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkstationOperatingComponent]:

        return db.scalar(

            select(WorkstationOperatingComponent).where(

                WorkstationOperatingComponent.business_id == business_id, WorkstationOperatingComponent.name == name

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

    ) -> tuple[Sequence[WorkstationOperatingComponent], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkstationOperatingComponent.business_id == business_id]

        if search:

            conditions.append(WorkstationOperatingComponent.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(WorkstationOperatingComponent).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkstationOperatingComponent)

            .where(*conditions)

            .order_by(WorkstationOperatingComponent.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: WorkstationOperatingComponent) -> WorkstationOperatingComponent:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: WorkstationOperatingComponent) -> None:

        db.delete(row)

        db.flush()
