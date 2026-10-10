"""Data access for SalesInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.sales_invoice_domain.models.sales_invoice import SalesInvoice

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoiceRepository"]





class SalesInvoiceRepository:

    model = SalesInvoice



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(SalesInvoice.items), selectinload(SalesInvoice.pricing_rules), selectinload(SalesInvoice.timesheets), selectinload(SalesInvoice.advances), selectinload(SalesInvoice.payments), selectinload(SalesInvoice.tax_withholding_entries)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoice]:

        return db.scalar(

            select(SalesInvoice).where(

                SalesInvoice.business_id == business_id, SalesInvoice.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SalesInvoice]:

        return db.scalar(

            select(SalesInvoice).where(

                SalesInvoice.business_id == business_id, SalesInvoice.name == name

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

    ) -> tuple[Sequence[SalesInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoice.business_id == business_id]

        if not include_cancelled:

            conditions.append(SalesInvoice.docstatus != 2)

        if search:

            conditions.append(SalesInvoice.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoice)

            .where(*conditions)

            .order_by(SalesInvoice.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: SalesInvoice) -> SalesInvoice:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SalesInvoice) -> None:

        db.delete(row)

        db.flush()
