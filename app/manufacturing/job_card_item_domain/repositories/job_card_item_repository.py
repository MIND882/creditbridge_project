"""Data access for JobCardItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_item_domain.models.job_card_item import JobCardItem

from app.core.pagination import normalise_paging



__all__ = ["JobCardItemRepository"]





class JobCardItemRepository:

    model = JobCardItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCardItem]:

        return db.scalar(

            select(JobCardItem).where(

                JobCardItem.business_id == business_id, JobCardItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCardItem]:

        return db.scalar(

            select(JobCardItem).where(

                JobCardItem.business_id == business_id, JobCardItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JobCardItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCardItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(JobCardItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(JobCardItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCardItem)

            .where(*conditions)

            .order_by(JobCardItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
