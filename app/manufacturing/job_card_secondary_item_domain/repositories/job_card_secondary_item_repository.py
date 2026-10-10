"""Data access for JobCardSecondaryItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_secondary_item_domain.models.job_card_secondary_item import JobCardSecondaryItem

from app.core.pagination import normalise_paging



__all__ = ["JobCardSecondaryItemRepository"]





class JobCardSecondaryItemRepository:

    model = JobCardSecondaryItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCardSecondaryItem]:

        return db.scalar(

            select(JobCardSecondaryItem).where(

                JobCardSecondaryItem.business_id == business_id, JobCardSecondaryItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCardSecondaryItem]:

        return db.scalar(

            select(JobCardSecondaryItem).where(

                JobCardSecondaryItem.business_id == business_id, JobCardSecondaryItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[JobCardSecondaryItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCardSecondaryItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(JobCardSecondaryItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(JobCardSecondaryItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCardSecondaryItem)

            .where(*conditions)

            .order_by(JobCardSecondaryItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
