"""Data access for SalesTeam. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.sales_team_domain.models.sales_team import SalesTeam

from app.core.pagination import normalise_paging



__all__ = ["SalesTeamRepository"]





class SalesTeamRepository:

    model = SalesTeam





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesTeam]:

        return db.scalar(

            select(SalesTeam).where(

                SalesTeam.business_id == business_id, SalesTeam.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesTeam]:

        return db.scalar(

            select(SalesTeam).where(

                SalesTeam.business_id == business_id, SalesTeam.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SalesTeam], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesTeam.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesTeam.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesTeam).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesTeam)

            .where(*conditions)

            .order_by(SalesTeam.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
