"""Data access for StockEntryDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_entry_detail_domain.models.stock_entry_detail import StockEntryDetail

from app.core.pagination import normalise_paging



__all__ = ["StockEntryDetailRepository"]





class StockEntryDetailRepository:

    model = StockEntryDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockEntryDetail]:

        return db.scalar(

            select(StockEntryDetail).where(

                StockEntryDetail.business_id == business_id, StockEntryDetail.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[StockEntryDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockEntryDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(StockEntryDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(StockEntryDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockEntryDetail)

            .where(*conditions)

            .order_by(StockEntryDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
