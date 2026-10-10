"""Data access for JobCardOperation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_operation_domain.models.job_card_operation import JobCardOperation

from app.core.pagination import normalise_paging



__all__ = ["JobCardOperationRepository"]





class JobCardOperationRepository:

    model = JobCardOperation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCardOperation]:

        return db.scalar(

            select(JobCardOperation).where(

                JobCardOperation.business_id == business_id, JobCardOperation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCardOperation]:

        return db.scalar(

            select(JobCardOperation).where(

                JobCardOperation.business_id == business_id, JobCardOperation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JobCardOperation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCardOperation.business_id == business_id]

        if parent_id is not None:

            conditions.append(JobCardOperation.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(JobCardOperation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCardOperation)

            .where(*conditions)

            .order_by(JobCardOperation.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
