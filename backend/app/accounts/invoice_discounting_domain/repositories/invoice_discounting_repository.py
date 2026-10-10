"""Data access for InvoiceDiscounting. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.invoice_discounting_domain.models.invoice_discounting import InvoiceDiscounting

from app.core.pagination import normalise_paging



__all__ = ["InvoiceDiscountingRepository"]





class InvoiceDiscountingRepository:

    model = InvoiceDiscounting



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(InvoiceDiscounting.invoices)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[InvoiceDiscounting]:

        return db.scalar(

            select(InvoiceDiscounting).where(

                InvoiceDiscounting.business_id == business_id, InvoiceDiscounting.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[InvoiceDiscounting]:

        return db.scalar(

            select(InvoiceDiscounting).where(

                InvoiceDiscounting.business_id == business_id, InvoiceDiscounting.name == name

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

    ) -> tuple[Sequence[InvoiceDiscounting], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [InvoiceDiscounting.business_id == business_id]

        if not include_cancelled:

            conditions.append(InvoiceDiscounting.docstatus != 2)

        if search:

            conditions.append(InvoiceDiscounting.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(InvoiceDiscounting).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(InvoiceDiscounting)

            .where(*conditions)

            .order_by(InvoiceDiscounting.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: InvoiceDiscounting) -> InvoiceDiscounting:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: InvoiceDiscounting) -> None:

        db.delete(row)

        db.flush()
