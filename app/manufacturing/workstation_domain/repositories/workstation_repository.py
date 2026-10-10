"""Data access for Workstation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.workstation_domain.models.workstation import Workstation

from app.core.pagination import normalise_paging



__all__ = ["WorkstationRepository"]





class WorkstationRepository:

    model = Workstation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Workstation]:

        return db.scalar(

            select(Workstation).where(

                Workstation.business_id == business_id, Workstation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Workstation]:

        return db.scalar(

            select(Workstation).where(

                Workstation.business_id == business_id, Workstation.name == name

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

    ) -> tuple[Sequence[Workstation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Workstation.business_id == business_id]

        if search:

            conditions.append(Workstation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Workstation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Workstation)

            .where(*conditions)

            .order_by(Workstation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Workstation) -> Workstation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Workstation) -> None:

        db.delete(row)

        db.flush()
