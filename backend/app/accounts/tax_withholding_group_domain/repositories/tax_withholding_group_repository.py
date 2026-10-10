"""Data access for TaxWithholdingGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_group_domain.models.tax_withholding_group import TaxWithholdingGroup

from app.core.pagination import normalise_paging



__all__ = ["TaxWithholdingGroupRepository"]





class TaxWithholdingGroupRepository:

    model = TaxWithholdingGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[TaxWithholdingGroup]:

        return db.scalar(

            select(TaxWithholdingGroup).where(

                TaxWithholdingGroup.business_id == business_id, TaxWithholdingGroup.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[TaxWithholdingGroup]:

        return db.scalar(

            select(TaxWithholdingGroup).where(

                TaxWithholdingGroup.business_id == business_id, TaxWithholdingGroup.name == name

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

    ) -> tuple[Sequence[TaxWithholdingGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxWithholdingGroup.business_id == business_id]

        if search:

            conditions.append(TaxWithholdingGroup.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(TaxWithholdingGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(TaxWithholdingGroup)

            .where(*conditions)

            .order_by(TaxWithholdingGroup.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: TaxWithholdingGroup) -> TaxWithholdingGroup:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: TaxWithholdingGroup) -> None:

        db.delete(row)

        db.flush()
