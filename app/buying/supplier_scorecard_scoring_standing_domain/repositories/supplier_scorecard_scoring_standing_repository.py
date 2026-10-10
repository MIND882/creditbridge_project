"""Data access for SupplierScorecardScoringStanding. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_standing_domain.models.supplier_scorecard_scoring_standing import SupplierScorecardScoringStanding

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardScoringStandingRepository"]





class SupplierScorecardScoringStandingRepository:

    model = SupplierScorecardScoringStanding





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardScoringStanding]:

        return db.scalar(

            select(SupplierScorecardScoringStanding).where(

                SupplierScorecardScoringStanding.business_id == business_id, SupplierScorecardScoringStanding.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardScoringStanding]:

        return db.scalar(

            select(SupplierScorecardScoringStanding).where(

                SupplierScorecardScoringStanding.business_id == business_id, SupplierScorecardScoringStanding.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SupplierScorecardScoringStanding], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardScoringStanding.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierScorecardScoringStanding.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardScoringStanding).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardScoringStanding)

            .where(*conditions)

            .order_by(SupplierScorecardScoringStanding.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
