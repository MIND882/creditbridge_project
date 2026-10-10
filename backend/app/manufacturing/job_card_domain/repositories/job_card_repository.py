"""Data access for JobCard. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.job_card_domain.models.job_card import JobCard

from app.core.pagination import normalise_paging



__all__ = ["JobCardRepository"]





class JobCardRepository:

    model = JobCard





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[JobCard]:

        return db.scalar(

            select(JobCard).where(

                JobCard.business_id == business_id, JobCard.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[JobCard]:

        return db.scalar(

            select(JobCard).where(

                JobCard.business_id == business_id, JobCard.name == name

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

    ) -> tuple[Sequence[JobCard], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [JobCard.business_id == business_id]

        if not include_cancelled:

            conditions.append(JobCard.docstatus != 2)

        if search:

            conditions.append(JobCard.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(JobCard).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(JobCard)

            .where(*conditions)

            .order_by(JobCard.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: JobCard) -> JobCard:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: JobCard) -> None:

        db.delete(row)

        db.flush()
