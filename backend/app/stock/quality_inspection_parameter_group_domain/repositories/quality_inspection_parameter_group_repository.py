"""Data access for QualityInspectionParameterGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quality_inspection_parameter_group_domain.models.quality_inspection_parameter_group import QualityInspectionParameterGroup

from app.core.pagination import normalise_paging



__all__ = ["QualityInspectionParameterGroupRepository"]





class QualityInspectionParameterGroupRepository:

    model = QualityInspectionParameterGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[QualityInspectionParameterGroup]:

        return db.scalar(

            select(QualityInspectionParameterGroup).where(

                QualityInspectionParameterGroup.business_id == business_id, QualityInspectionParameterGroup.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[QualityInspectionParameterGroup]:

        return db.scalar(

            select(QualityInspectionParameterGroup).where(

                QualityInspectionParameterGroup.business_id == business_id, QualityInspectionParameterGroup.name == name

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

    ) -> tuple[Sequence[QualityInspectionParameterGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [QualityInspectionParameterGroup.business_id == business_id]

        if search:

            conditions.append(QualityInspectionParameterGroup.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(QualityInspectionParameterGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(QualityInspectionParameterGroup)

            .where(*conditions)

            .order_by(QualityInspectionParameterGroup.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: QualityInspectionParameterGroup) -> QualityInspectionParameterGroup:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: QualityInspectionParameterGroup) -> None:

        db.delete(row)

        db.flush()
