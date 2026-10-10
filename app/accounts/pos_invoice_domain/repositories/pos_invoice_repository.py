"""Data access for POSInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_invoice_domain.models.pos_invoice import POSInvoice

from app.core.pagination import normalise_paging



__all__ = ["POSInvoiceRepository"]





class POSInvoiceRepository:

    model = POSInvoice



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSInvoice.items), selectinload(POSInvoice.pricing_rules), selectinload(POSInvoice.timesheets), selectinload(POSInvoice.advances), selectinload(POSInvoice.payments)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSInvoice]:

        return db.scalar(

            select(POSInvoice).where(

                POSInvoice.business_id == business_id, POSInvoice.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSInvoice]:

        return db.scalar(

            select(POSInvoice).where(

                POSInvoice.business_id == business_id, POSInvoice.name == name

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

    ) -> tuple[Sequence[POSInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSInvoice.business_id == business_id]

        if not include_cancelled:

            conditions.append(POSInvoice.docstatus != 2)

        if search:

            conditions.append(POSInvoice.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSInvoice)

            .where(*conditions)

            .order_by(POSInvoice.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSInvoice) -> POSInvoice:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSInvoice) -> None:

        db.delete(row)

        db.flush()
