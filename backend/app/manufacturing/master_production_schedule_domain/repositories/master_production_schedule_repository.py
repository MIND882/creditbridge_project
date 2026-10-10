"""Data access for MasterProductionSchedule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.master_production_schedule_domain.models.master_production_schedule import MasterProductionSchedule

from app.core.pagination import normalise_paging



__all__ = ["MasterProductionScheduleRepository"]





class MasterProductionScheduleRepository:

    model = MasterProductionSchedule





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MasterProductionSchedule]:

        return db.scalar(

            select(MasterProductionSchedule).where(

                MasterProductionSchedule.business_id == business_id, MasterProductionSchedule.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[MasterProductionSchedule]:

        return db.scalar(

            select(MasterProductionSchedule).where(

                MasterProductionSchedule.business_id == business_id, MasterProductionSchedule.name == name

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

    ) -> tuple[Sequence[MasterProductionSchedule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MasterProductionSchedule.business_id == business_id]

        if search:

            conditions.append(MasterProductionSchedule.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(MasterProductionSchedule).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MasterProductionSchedule)

            .where(*conditions)

            .order_by(MasterProductionSchedule.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: MasterProductionSchedule) -> MasterProductionSchedule:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: MasterProductionSchedule) -> None:

        db.delete(row)

        db.flush()
