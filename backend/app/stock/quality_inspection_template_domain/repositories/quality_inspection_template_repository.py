"""Data access for QualityInspectionTemplate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_template_domain.models.quality_inspection_template import QualityInspectionTemplate

from app.core.pagination import normalise_paging



__all__ = ["QualityInspectionTemplateRepository"]





class QualityInspectionTemplateRepository:

    model = QualityInspectionTemplate





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[QualityInspectionTemplate]:

        return db.scalar(

            select(QualityInspectionTemplate).where(

                QualityInspectionTemplate.business_id == business_id, QualityInspectionTemplate.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[QualityInspectionTemplate]:

        return db.scalar(

            select(QualityInspectionTemplate).where(

                QualityInspectionTemplate.business_id == business_id, QualityInspectionTemplate.name == name

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

    ) -> tuple[Sequence[QualityInspectionTemplate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [QualityInspectionTemplate.business_id == business_id]

        if search:

            conditions.append(QualityInspectionTemplate.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(QualityInspectionTemplate).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(QualityInspectionTemplate)

            .where(*conditions)

            .order_by(QualityInspectionTemplate.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: QualityInspectionTemplate) -> QualityInspectionTemplate:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: QualityInspectionTemplate) -> None:

        db.delete(row)

        db.flush()
