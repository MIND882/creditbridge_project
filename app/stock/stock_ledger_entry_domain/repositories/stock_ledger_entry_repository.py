"""Data access for StockLedgerEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_ledger_entry_domain.models.stock_ledger_entry import StockLedgerEntry

from app.core.pagination import normalise_paging



__all__ = ["StockLedgerEntryRepository"]





class StockLedgerEntryRepository:

    model = StockLedgerEntry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockLedgerEntry]:

        return db.scalar(

            select(StockLedgerEntry).where(

                StockLedgerEntry.business_id == business_id, StockLedgerEntry.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockLedgerEntry]:

        return db.scalar(

            select(StockLedgerEntry).where(

                StockLedgerEntry.business_id == business_id, StockLedgerEntry.name == name

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

    ) -> tuple[Sequence[StockLedgerEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockLedgerEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(StockLedgerEntry.docstatus != 2)

        if search:

            conditions.append(StockLedgerEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(StockLedgerEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockLedgerEntry)

            .where(*conditions)

            .order_by(StockLedgerEntry.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: StockLedgerEntry) -> StockLedgerEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: StockLedgerEntry) -> None:

        db.delete(row)

        db.flush()
