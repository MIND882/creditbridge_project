"""Data access for QualityInspectionReading. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_reading_domain.models.quality_inspection_reading import QualityInspectionReading

from app.core.pagination import normalise_paging



__all__ = ["QualityInspectionReadingRepository"]





class QualityInspectionReadingRepository:

    model = QualityInspectionReading





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[QualityInspectionReading]:

        return db.scalar(

            select(QualityInspectionReading).where(

                QualityInspectionReading.business_id == business_id, QualityInspectionReading.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[QualityInspectionReading], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [QualityInspectionReading.business_id == business_id]

        if parent_id is not None:

            conditions.append(QualityInspectionReading.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(QualityInspectionReading).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(QualityInspectionReading)

            .where(*conditions)

            .order_by(QualityInspectionReading.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
