"""Data access for POSClosingEntryTaxes. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_closing_entry_taxes_domain.models.pos_closing_entry_taxes import POSClosingEntryTaxes

from app.core.pagination import normalise_paging



__all__ = ["POSClosingEntryTaxesRepository"]





class POSClosingEntryTaxesRepository:

    model = POSClosingEntryTaxes





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSClosingEntryTaxes]:

        return db.scalar(

            select(POSClosingEntryTaxes).where(

                POSClosingEntryTaxes.business_id == business_id, POSClosingEntryTaxes.id == row_id

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

    ) -> tuple[Sequence[POSClosingEntryTaxes], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSClosingEntryTaxes.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSClosingEntryTaxes.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSClosingEntryTaxes).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSClosingEntryTaxes)

            .where(*conditions)

            .order_by(POSClosingEntryTaxes.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


