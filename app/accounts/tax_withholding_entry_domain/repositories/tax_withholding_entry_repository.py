"""Data access for TaxWithholdingEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry

from app.core.pagination import normalise_paging



__all__ = ["TaxWithholdingEntryRepository"]





class TaxWithholdingEntryRepository:

    model = TaxWithholdingEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[TaxWithholdingEntry]:

        return db.scalar(

            select(TaxWithholdingEntry).where(

                TaxWithholdingEntry.business_id == business_id, TaxWithholdingEntry.id == row_id

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

    ) -> tuple[Sequence[TaxWithholdingEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [TaxWithholdingEntry.business_id == business_id]

        if parent_id is not None:

            conditions.append(TaxWithholdingEntry.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(TaxWithholdingEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(TaxWithholdingEntry)

            .where(*conditions)

            .order_by(TaxWithholdingEntry.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


