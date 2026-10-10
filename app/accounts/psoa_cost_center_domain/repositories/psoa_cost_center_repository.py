"""Data access for PsoaCostCenter. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.psoa_cost_center_domain.models.psoa_cost_center import PsoaCostCenter

from app.core.pagination import normalise_paging



__all__ = ["PsoaCostCenterRepository"]





class PsoaCostCenterRepository:

    model = PsoaCostCenter





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PsoaCostCenter]:

        return db.scalar(

            select(PsoaCostCenter).where(

                PsoaCostCenter.business_id == business_id, PsoaCostCenter.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PsoaCostCenter], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PsoaCostCenter.business_id == business_id]

        if parent_id is not None:

            conditions.append(PsoaCostCenter.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PsoaCostCenter).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PsoaCostCenter)

            .where(*conditions)

            .order_by(PsoaCostCenter.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


