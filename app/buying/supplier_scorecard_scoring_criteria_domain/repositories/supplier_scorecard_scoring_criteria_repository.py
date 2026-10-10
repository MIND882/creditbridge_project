"""Data access for SupplierScorecardScoringCriteria. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_criteria_domain.models.supplier_scorecard_scoring_criteria import SupplierScorecardScoringCriteria

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardScoringCriteriaRepository"]





class SupplierScorecardScoringCriteriaRepository:

    model = SupplierScorecardScoringCriteria





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardScoringCriteria]:

        return db.scalar(

            select(SupplierScorecardScoringCriteria).where(

                SupplierScorecardScoringCriteria.business_id == business_id, SupplierScorecardScoringCriteria.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardScoringCriteria]:

        return db.scalar(

            select(SupplierScorecardScoringCriteria).where(

                SupplierScorecardScoringCriteria.business_id == business_id, SupplierScorecardScoringCriteria.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SupplierScorecardScoringCriteria], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardScoringCriteria.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierScorecardScoringCriteria.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardScoringCriteria).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardScoringCriteria)

            .where(*conditions)

            .order_by(SupplierScorecardScoringCriteria.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
