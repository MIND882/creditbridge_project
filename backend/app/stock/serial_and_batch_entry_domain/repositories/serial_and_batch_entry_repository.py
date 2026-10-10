"""Data access for SerialAndBatchEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.serial_and_batch_entry_domain.models.serial_and_batch_entry import SerialAndBatchEntry

from app.core.pagination import normalise_paging



__all__ = ["SerialAndBatchEntryRepository"]





class SerialAndBatchEntryRepository:

    model = SerialAndBatchEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SerialAndBatchEntry]:

        return db.scalar(

            select(SerialAndBatchEntry).where(

                SerialAndBatchEntry.business_id == business_id, SerialAndBatchEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SerialAndBatchEntry]:

        return db.scalar(

            select(SerialAndBatchEntry).where(

                SerialAndBatchEntry.business_id == business_id, SerialAndBatchEntry.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SerialAndBatchEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SerialAndBatchEntry.business_id == business_id]

        if parent_id is not None:

            conditions.append(SerialAndBatchEntry.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SerialAndBatchEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SerialAndBatchEntry)

            .where(*conditions)

            .order_by(SerialAndBatchEntry.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
