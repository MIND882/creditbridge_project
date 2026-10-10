"""Data access for SupplierScorecardStanding. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_standing_domain.models.supplier_scorecard_standing import SupplierScorecardStanding

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardStandingRepository"]





class SupplierScorecardStandingRepository:

    model = SupplierScorecardStanding





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardStanding]:

        return db.scalar(

            select(SupplierScorecardStanding).where(

                SupplierScorecardStanding.business_id == business_id, SupplierScorecardStanding.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardStanding]:

        return db.scalar(

            select(SupplierScorecardStanding).where(

                SupplierScorecardStanding.business_id == business_id, SupplierScorecardStanding.name == name

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

    ) -> tuple[Sequence[SupplierScorecardStanding], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardStanding.business_id == business_id]

        if search:

            conditions.append(SupplierScorecardStanding.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardStanding).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardStanding)

            .where(*conditions)

            .order_by(SupplierScorecardStanding.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierScorecardStanding) -> SupplierScorecardStanding:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierScorecardStanding) -> None:

        db.delete(row)

        db.flush()
