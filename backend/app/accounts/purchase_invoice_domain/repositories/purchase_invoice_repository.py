"""Data access for PurchaseInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.purchase_invoice_domain.models.purchase_invoice import PurchaseInvoice

from app.core.pagination import normalise_paging



__all__ = ["PurchaseInvoiceRepository"]





class PurchaseInvoiceRepository:

    model = PurchaseInvoice



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PurchaseInvoice.items), selectinload(PurchaseInvoice.pricing_rules), selectinload(PurchaseInvoice.advances), selectinload(PurchaseInvoice.tax_withholding_entries)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseInvoice]:

        return db.scalar(

            select(PurchaseInvoice).where(

                PurchaseInvoice.business_id == business_id, PurchaseInvoice.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseInvoice]:

        return db.scalar(

            select(PurchaseInvoice).where(

                PurchaseInvoice.business_id == business_id, PurchaseInvoice.name == name

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

    ) -> tuple[Sequence[PurchaseInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseInvoice.business_id == business_id]

        if not include_cancelled:

            conditions.append(PurchaseInvoice.docstatus != 2)

        if search:

            conditions.append(PurchaseInvoice.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseInvoice)

            .where(*conditions)

            .order_by(PurchaseInvoice.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PurchaseInvoice) -> PurchaseInvoice:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PurchaseInvoice) -> None:

        db.delete(row)

        db.flush()
