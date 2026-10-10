"""Data access for JobCardTimeLog. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_time_log_domain.models.job_card_time_log import JobCardTimeLog

from app.core.pagination import normalise_paging



__all__ = ["JobCardTimeLogRepository"]





class JobCardTimeLogRepository:

    model = JobCardTimeLog





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCardTimeLog]:

        return db.scalar(

            select(JobCardTimeLog).where(

                JobCardTimeLog.business_id == business_id, JobCardTimeLog.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCardTimeLog]:

        return db.scalar(

            select(JobCardTimeLog).where(

                JobCardTimeLog.business_id == business_id, JobCardTimeLog.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JobCardTimeLog], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCardTimeLog.business_id == business_id]

        if parent_id is not None:

            conditions.append(JobCardTimeLog.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(JobCardTimeLog).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCardTimeLog)

            .where(*conditions)

            .order_by(JobCardTimeLog.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
