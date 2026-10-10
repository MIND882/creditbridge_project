"""Data access for SupplierScorecardPeriod. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_period_domain.models.supplier_scorecard_period import SupplierScorecardPeriod

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardPeriodRepository"]





class SupplierScorecardPeriodRepository:

    model = SupplierScorecardPeriod





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardPeriod]:

        return db.scalar(

            select(SupplierScorecardPeriod).where(

                SupplierScorecardPeriod.business_id == business_id, SupplierScorecardPeriod.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardPeriod]:

        return db.scalar(

            select(SupplierScorecardPeriod).where(

                SupplierScorecardPeriod.business_id == business_id, SupplierScorecardPeriod.name == name

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

    ) -> tuple[Sequence[SupplierScorecardPeriod], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardPeriod.business_id == business_id]

        if search:

            conditions.append(SupplierScorecardPeriod.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardPeriod).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardPeriod)

            .where(*conditions)

            .order_by(SupplierScorecardPeriod.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierScorecardPeriod) -> SupplierScorecardPeriod:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierScorecardPeriod) -> None:

        db.delete(row)

        db.flush()
