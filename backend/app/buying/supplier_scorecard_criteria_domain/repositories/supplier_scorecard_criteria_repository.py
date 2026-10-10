"""Data access for SupplierScorecardCriteria. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_criteria_domain.models.supplier_scorecard_criteria import SupplierScorecardCriteria

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardCriteriaRepository"]





class SupplierScorecardCriteriaRepository:

    model = SupplierScorecardCriteria





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardCriteria]:

        return db.scalar(

            select(SupplierScorecardCriteria).where(

                SupplierScorecardCriteria.business_id == business_id, SupplierScorecardCriteria.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardCriteria]:

        return db.scalar(

            select(SupplierScorecardCriteria).where(

                SupplierScorecardCriteria.business_id == business_id, SupplierScorecardCriteria.name == name

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

    ) -> tuple[Sequence[SupplierScorecardCriteria], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardCriteria.business_id == business_id]

        if search:

            conditions.append(SupplierScorecardCriteria.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardCriteria).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardCriteria)

            .where(*conditions)

            .order_by(SupplierScorecardCriteria.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierScorecardCriteria) -> SupplierScorecardCriteria:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierScorecardCriteria) -> None:

        db.delete(row)

        db.flush()
