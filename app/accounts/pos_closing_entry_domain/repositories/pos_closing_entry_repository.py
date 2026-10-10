"""Data access for POSClosingEntry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_closing_entry_domain.models.pos_closing_entry import POSClosingEntry

from app.core.pagination import normalise_paging



__all__ = ["POSClosingEntryRepository"]





class POSClosingEntryRepository:

    model = POSClosingEntry



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSClosingEntry.payment_reconciliation), selectinload(POSClosingEntry.taxes), selectinload(POSClosingEntry.pos_invoices), selectinload(POSClosingEntry.sales_invoices)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSClosingEntry]:

        return db.scalar(

            select(POSClosingEntry).where(

                POSClosingEntry.business_id == business_id, POSClosingEntry.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSClosingEntry]:

        return db.scalar(

            select(POSClosingEntry).where(

                POSClosingEntry.business_id == business_id, POSClosingEntry.name == name

            ).options(*self._options())

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

    ) -> tuple[Sequence[POSClosingEntry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSClosingEntry.business_id == business_id]

        if not include_cancelled:

            conditions.append(POSClosingEntry.docstatus != 2)

        if search:

            conditions.append(POSClosingEntry.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSClosingEntry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSClosingEntry)

            .where(*conditions)

            .order_by(POSClosingEntry.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSClosingEntry) -> POSClosingEntry:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSClosingEntry) -> None:

        db.delete(row)

        db.flush()
