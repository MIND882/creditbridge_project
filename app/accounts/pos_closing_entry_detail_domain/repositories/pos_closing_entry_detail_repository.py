"""Data access for POSClosingEntryDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_closing_entry_detail_domain.models.pos_closing_entry_detail import POSClosingEntryDetail

from app.core.pagination import normalise_paging



__all__ = ["POSClosingEntryDetailRepository"]





class POSClosingEntryDetailRepository:

    model = POSClosingEntryDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSClosingEntryDetail]:

        return db.scalar(

            select(POSClosingEntryDetail).where(

                POSClosingEntryDetail.business_id == business_id, POSClosingEntryDetail.id == row_id

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

    ) -> tuple[Sequence[POSClosingEntryDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSClosingEntryDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSClosingEntryDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSClosingEntryDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSClosingEntryDetail)

            .where(*conditions)

            .order_by(POSClosingEntryDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


