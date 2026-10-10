"""Data access for StockEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_entry_domain.models.stock_entry import StockEntry

from app.core.pagination import normalise_paging



__all__ = ["StockEntryRepository"]





class StockEntryRepository:

    model = StockEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockEntry]:

        return db.scalar(

            select(StockEntry).where(

                StockEntry.business_id == business_id, StockEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockEntry]:

        return db.scalar(

            select(StockEntry).where(

                StockEntry.business_id == business_id, StockEntry.name == name

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

    ) -> tuple[Sequence[StockEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(StockEntry.docstatus != 2)

        if search:

            conditions.append(StockEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(StockEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockEntry)

            .where(*conditions)

            .order_by(StockEntry.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: StockEntry) -> StockEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: StockEntry) -> None:

        db.delete(row)

        db.flush()
