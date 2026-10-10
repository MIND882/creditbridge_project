"""Data access for Batch. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.batch_domain.models.batch import Batch

from app.core.pagination import normalise_paging



__all__ = ["BatchRepository"]





class BatchRepository:

    model = Batch





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Batch]:

        return db.scalar(

            select(Batch).where(

                Batch.business_id == business_id, Batch.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Batch]:

        return db.scalar(

            select(Batch).where(

                Batch.business_id == business_id, Batch.name == name

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

    ) -> tuple[Sequence[Batch], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Batch.business_id == business_id]

        if search:

            conditions.append(Batch.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Batch).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Batch)

            .where(*conditions)

            .order_by(Batch.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Batch) -> Batch:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Batch) -> None:

        db.delete(row)

        db.flush()
