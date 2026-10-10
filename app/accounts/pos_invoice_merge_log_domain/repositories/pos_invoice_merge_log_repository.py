"""Data access for POSInvoiceMergeLog. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pos_invoice_merge_log_domain.models.pos_invoice_merge_log import POSInvoiceMergeLog

from app.core.pagination import normalise_paging



__all__ = ["POSInvoiceMergeLogRepository"]





class POSInvoiceMergeLogRepository:

    model = POSInvoiceMergeLog



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(POSInvoiceMergeLog.pos_invoices)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSInvoiceMergeLog]:

        return db.scalar(

            select(POSInvoiceMergeLog).where(

                POSInvoiceMergeLog.business_id == business_id, POSInvoiceMergeLog.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[POSInvoiceMergeLog]:

        return db.scalar(

            select(POSInvoiceMergeLog).where(

                POSInvoiceMergeLog.business_id == business_id, POSInvoiceMergeLog.name == name

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

    ) -> tuple[Sequence[POSInvoiceMergeLog], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSInvoiceMergeLog.business_id == business_id]

        if not include_cancelled:

            conditions.append(POSInvoiceMergeLog.docstatus != 2)

        if search:

            conditions.append(POSInvoiceMergeLog.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(POSInvoiceMergeLog).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSInvoiceMergeLog)

            .where(*conditions)

            .order_by(POSInvoiceMergeLog.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: POSInvoiceMergeLog) -> POSInvoiceMergeLog:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: POSInvoiceMergeLog) -> None:

        db.delete(row)

        db.flush()
