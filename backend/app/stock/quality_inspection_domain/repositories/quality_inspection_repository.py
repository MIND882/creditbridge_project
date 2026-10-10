"""Data access for QualityInspection. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_domain.models.quality_inspection import QualityInspection

from app.core.pagination import normalise_paging



__all__ = ["QualityInspectionRepository"]





class QualityInspectionRepository:

    model = QualityInspection





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[QualityInspection]:

        return db.scalar(

            select(QualityInspection).where(

                QualityInspection.business_id == business_id, QualityInspection.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[QualityInspection]:

        return db.scalar(

            select(QualityInspection).where(

                QualityInspection.business_id == business_id, QualityInspection.name == name

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

    ) -> tuple[Sequence[QualityInspection], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [QualityInspection.business_id == business_id]

        if not include_cancelled:

            conditions.append(QualityInspection.docstatus != 2)

        if search:

            conditions.append(QualityInspection.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(QualityInspection).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(QualityInspection)

            .where(*conditions)

            .order_by(QualityInspection.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: QualityInspection) -> QualityInspection:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: QualityInspection) -> None:

        db.delete(row)

        db.flush()
