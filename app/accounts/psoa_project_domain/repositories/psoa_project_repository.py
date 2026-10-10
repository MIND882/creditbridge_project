"""Data access for PsoaProject. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.psoa_project_domain.models.psoa_project import PsoaProject

from app.core.pagination import normalise_paging



__all__ = ["PsoaProjectRepository"]





class PsoaProjectRepository:

    model = PsoaProject





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PsoaProject]:

        return db.scalar(

            select(PsoaProject).where(

                PsoaProject.business_id == business_id, PsoaProject.id == row_id

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

    ) -> tuple[Sequence[PsoaProject], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PsoaProject.business_id == business_id]

        if parent_id is not None:

            conditions.append(PsoaProject.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PsoaProject).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PsoaProject)

            .where(*conditions)

            .order_by(PsoaProject.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


