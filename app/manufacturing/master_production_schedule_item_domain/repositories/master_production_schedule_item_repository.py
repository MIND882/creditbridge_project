"""Data access for MasterProductionScheduleItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.master_production_schedule_item_domain.models.master_production_schedule_item import MasterProductionScheduleItem

from app.core.pagination import normalise_paging



__all__ = ["MasterProductionScheduleItemRepository"]





class MasterProductionScheduleItemRepository:

    model = MasterProductionScheduleItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MasterProductionScheduleItem]:

        return db.scalar(

            select(MasterProductionScheduleItem).where(

                MasterProductionScheduleItem.business_id == business_id, MasterProductionScheduleItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[MasterProductionScheduleItem]:

        return db.scalar(

            select(MasterProductionScheduleItem).where(

                MasterProductionScheduleItem.business_id == business_id, MasterProductionScheduleItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[MasterProductionScheduleItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MasterProductionScheduleItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(MasterProductionScheduleItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(MasterProductionScheduleItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MasterProductionScheduleItem)

            .where(*conditions)

            .order_by(MasterProductionScheduleItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
