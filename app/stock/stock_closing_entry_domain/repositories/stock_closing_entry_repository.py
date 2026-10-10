"""Data access for StockClosingEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_closing_entry_domain.models.stock_closing_entry import StockClosingEntry

from app.core.pagination import normalise_paging



__all__ = ["StockClosingEntryRepository"]





class StockClosingEntryRepository:

    model = StockClosingEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockClosingEntry]:

        return db.scalar(

            select(StockClosingEntry).where(

                StockClosingEntry.business_id == business_id, StockClosingEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockClosingEntry]:

        return db.scalar(

            select(StockClosingEntry).where(

                StockClosingEntry.business_id == business_id, StockClosingEntry.name == name

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

    ) -> tuple[Sequence[StockClosingEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockClosingEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(StockClosingEntry.docstatus != 2)

        if search:

            conditions.append(StockClosingEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(StockClosingEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockClosingEntry)

            .where(*conditions)

            .order_by(StockClosingEntry.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: StockClosingEntry) -> StockClosingEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: StockClosingEntry) -> None:

        db.delete(row)

        db.flush()
