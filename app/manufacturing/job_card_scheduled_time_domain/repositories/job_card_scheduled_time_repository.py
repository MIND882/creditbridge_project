"""Data access for JobCardScheduledTime. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_scheduled_time_domain.models.job_card_scheduled_time import JobCardScheduledTime

from app.core.pagination import normalise_paging



__all__ = ["JobCardScheduledTimeRepository"]





class JobCardScheduledTimeRepository:

    model = JobCardScheduledTime





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCardScheduledTime]:

        return db.scalar(

            select(JobCardScheduledTime).where(

                JobCardScheduledTime.business_id == business_id, JobCardScheduledTime.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCardScheduledTime]:

        return db.scalar(

            select(JobCardScheduledTime).where(

                JobCardScheduledTime.business_id == business_id, JobCardScheduledTime.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JobCardScheduledTime], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCardScheduledTime.business_id == business_id]

        if parent_id is not None:

            conditions.append(JobCardScheduledTime.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(JobCardScheduledTime).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCardScheduledTime)

            .where(*conditions)

            .order_by(JobCardScheduledTime.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
