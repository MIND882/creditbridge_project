"""Data access for SupplierScorecardVariable. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_variable_domain.models.supplier_scorecard_variable import SupplierScorecardVariable

from app.core.pagination import normalise_paging



__all__ = ["SupplierScorecardVariableRepository"]





class SupplierScorecardVariableRepository:

    model = SupplierScorecardVariable





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierScorecardVariable]:

        return db.scalar(

            select(SupplierScorecardVariable).where(

                SupplierScorecardVariable.business_id == business_id, SupplierScorecardVariable.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierScorecardVariable]:

        return db.scalar(

            select(SupplierScorecardVariable).where(

                SupplierScorecardVariable.business_id == business_id, SupplierScorecardVariable.name == name

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

    ) -> tuple[Sequence[SupplierScorecardVariable], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierScorecardVariable.business_id == business_id]

        if search:

            conditions.append(SupplierScorecardVariable.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierScorecardVariable).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierScorecardVariable)

            .where(*conditions)

            .order_by(SupplierScorecardVariable.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierScorecardVariable) -> SupplierScorecardVariable:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierScorecardVariable) -> None:

        db.delete(row)

        db.flush()
