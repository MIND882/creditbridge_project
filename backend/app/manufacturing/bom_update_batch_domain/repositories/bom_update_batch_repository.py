"""Data access for BomUpdateBatch. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.bom_update_batch_domain.models.bom_update_batch import BomUpdateBatch

from app.core.pagination import normalise_paging



__all__ = ["BomUpdateBatchRepository"]





class BomUpdateBatchRepository:

    model = BomUpdateBatch





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BomUpdateBatch]:

        return db.scalar(

            select(BomUpdateBatch).where(

                BomUpdateBatch.business_id == business_id, BomUpdateBatch.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[BomUpdateBatch], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BomUpdateBatch.business_id == business_id]

        if parent_id is not None:

            conditions.append(BomUpdateBatch.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BomUpdateBatch).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BomUpdateBatch)

            .where(*conditions)

            .order_by(BomUpdateBatch.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
