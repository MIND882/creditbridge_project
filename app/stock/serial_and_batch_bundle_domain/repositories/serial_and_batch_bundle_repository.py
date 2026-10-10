"""Data access for SerialAndBatchBundle. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.serial_and_batch_bundle_domain.models.serial_and_batch_bundle import SerialAndBatchBundle

from app.core.pagination import normalise_paging



__all__ = ["SerialAndBatchBundleRepository"]





class SerialAndBatchBundleRepository:

    model = SerialAndBatchBundle





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SerialAndBatchBundle]:

        return db.scalar(

            select(SerialAndBatchBundle).where(

                SerialAndBatchBundle.business_id == business_id, SerialAndBatchBundle.id == row_id

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

    ) -> tuple[Sequence[SerialAndBatchBundle], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SerialAndBatchBundle.business_id == business_id]

        if not include_cancelled:

            conditions.append(SerialAndBatchBundle.docstatus != 2)

        if search:

            conditions.append(SerialAndBatchBundle.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SerialAndBatchBundle).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SerialAndBatchBundle)

            .where(*conditions)

            .order_by(SerialAndBatchBundle.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SerialAndBatchBundle) -> SerialAndBatchBundle:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SerialAndBatchBundle) -> None:

        db.delete(row)

        db.flush()
