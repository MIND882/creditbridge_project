"""Data access for TaxWithholdingRate. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_rate_domain.models.tax_withholding_rate import TaxWithholdingRate

from app.core.pagination import normalise_paging



__all__ = ["TaxWithholdingRateRepository"]





class TaxWithholdingRateRepository:

    model = TaxWithholdingRate



    def get_by_id(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> Optional[TaxWithholdingRate]:

        return db.scalar(

            select(TaxWithholdingRate).where(

                TaxWithholdingRate.business_id == business_id, TaxWithholdingRate.id == row_id

            )

        )



    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[TaxWithholdingRate], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxWithholdingRate.business_id == business_id]

        if parent_id is not None:

            conditions.append(TaxWithholdingRate.parent_id == parent_id)

        total = int(

            db.scalar(select(func.count()).select_from(TaxWithholdingRate).where(*conditions)) or 0

        )

        rows = db.scalars(

            select(TaxWithholdingRate)

            .where(*conditions)

            .order_by(TaxWithholdingRate.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
