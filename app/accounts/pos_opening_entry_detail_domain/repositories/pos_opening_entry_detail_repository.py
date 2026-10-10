"""Data access for POSOpeningEntryDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_opening_entry_detail_domain.models.pos_opening_entry_detail import POSOpeningEntryDetail

from app.core.pagination import normalise_paging



__all__ = ["POSOpeningEntryDetailRepository"]





class POSOpeningEntryDetailRepository:

    model = POSOpeningEntryDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSOpeningEntryDetail]:

        return db.scalar(

            select(POSOpeningEntryDetail).where(

                POSOpeningEntryDetail.business_id == business_id, POSOpeningEntryDetail.id == row_id

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

    ) -> tuple[Sequence[POSOpeningEntryDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSOpeningEntryDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSOpeningEntryDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSOpeningEntryDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSOpeningEntryDetail)

            .where(*conditions)

            .order_by(POSOpeningEntryDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


