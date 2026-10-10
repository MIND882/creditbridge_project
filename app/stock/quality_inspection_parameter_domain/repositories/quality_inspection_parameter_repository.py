"""Data access for QualityInspectionParameter. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_parameter_domain.models.quality_inspection_parameter import QualityInspectionParameter

from app.core.pagination import normalise_paging



__all__ = ["QualityInspectionParameterRepository"]





class QualityInspectionParameterRepository:

    model = QualityInspectionParameter





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[QualityInspectionParameter]:

        return db.scalar(

            select(QualityInspectionParameter).where(

                QualityInspectionParameter.business_id == business_id, QualityInspectionParameter.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[QualityInspectionParameter]:

        return db.scalar(

            select(QualityInspectionParameter).where(

                QualityInspectionParameter.business_id == business_id, QualityInspectionParameter.name == name

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

    ) -> tuple[Sequence[QualityInspectionParameter], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [QualityInspectionParameter.business_id == business_id]

        if search:

            conditions.append(QualityInspectionParameter.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(QualityInspectionParameter).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(QualityInspectionParameter)

            .where(*conditions)

            .order_by(QualityInspectionParameter.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: QualityInspectionParameter) -> QualityInspectionParameter:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: QualityInspectionParameter) -> None:

        db.delete(row)

        db.flush()
