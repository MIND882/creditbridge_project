"""Data access for SupplierScorecard. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_domain.models.supplier_scorecard import SupplierScorecard

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardRepository"]





class SupplierScorecardRepository:

    model = SupplierScorecard





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecard]:

        return db.scalar(

            select(SupplierScorecard).where(

                SupplierScorecard.business_id == business_id, SupplierScorecard.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecard]:

        return db.scalar(

            select(SupplierScorecard).where(

                SupplierScorecard.business_id == business_id, SupplierScorecard.name == name

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

    ) -> tuple[Sequence[SupplierScorecard], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecard.business_id == business_id]

        if search:

            conditions.append(SupplierScorecard.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecard).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecard)

            .where(*conditions)

            .order_by(SupplierScorecard.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierScorecard) -> SupplierScorecard:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierScorecard) -> None:

        db.delete(row)

        db.flush()
