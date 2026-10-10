"""Data access for SupplierScorecardScoringVariable. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_variable_domain.models.supplier_scorecard_scoring_variable import SupplierScorecardScoringVariable

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardScoringVariableRepository"]





class SupplierScorecardScoringVariableRepository:

    model = SupplierScorecardScoringVariable





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardScoringVariable]:

        return db.scalar(

            select(SupplierScorecardScoringVariable).where(

                SupplierScorecardScoringVariable.business_id == business_id, SupplierScorecardScoringVariable.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardScoringVariable]:

        return db.scalar(

            select(SupplierScorecardScoringVariable).where(

                SupplierScorecardScoringVariable.business_id == business_id, SupplierScorecardScoringVariable.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SupplierScorecardScoringVariable], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardScoringVariable.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierScorecardScoringVariable.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardScoringVariable).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardScoringVariable)

            .where(*conditions)

            .order_by(SupplierScorecardScoringVariable.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
