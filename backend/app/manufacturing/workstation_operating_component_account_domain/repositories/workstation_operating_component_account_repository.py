"""Data access for WorkstationOperatingComponentAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_operating_component_account_domain.models.workstation_operating_component_account import WorkstationOperatingComponentAccount

from app.core.pagination import normalise_paging



__all__ = ["WorkstationOperatingComponentAccountRepository"]





class WorkstationOperatingComponentAccountRepository:

    model = WorkstationOperatingComponentAccount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[WorkstationOperatingComponentAccount]:

        return db.scalar(

            select(WorkstationOperatingComponentAccount).where(

                WorkstationOperatingComponentAccount.business_id == business_id, WorkstationOperatingComponentAccount.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[WorkstationOperatingComponentAccount]:

        return db.scalar(

            select(WorkstationOperatingComponentAccount).where(

                WorkstationOperatingComponentAccount.business_id == business_id, WorkstationOperatingComponentAccount.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[WorkstationOperatingComponentAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [WorkstationOperatingComponentAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(WorkstationOperatingComponentAccount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(WorkstationOperatingComponentAccount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(WorkstationOperatingComponentAccount)

            .where(*conditions)

            .order_by(WorkstationOperatingComponentAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
