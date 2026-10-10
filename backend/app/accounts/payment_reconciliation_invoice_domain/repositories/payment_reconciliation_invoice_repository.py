"""Data access for PaymentReconciliationInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.payment_reconciliation_invoice_domain.models.payment_reconciliation_invoice import PaymentReconciliationInvoice

from app.core.pagination import normalise_paging



__all__ = ["PaymentReconciliationInvoiceRepository"]





class PaymentReconciliationInvoiceRepository:

    model = PaymentReconciliationInvoice





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PaymentReconciliationInvoice]:

        return db.scalar(

            select(PaymentReconciliationInvoice).where(

                PaymentReconciliationInvoice.business_id == business_id, PaymentReconciliationInvoice.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PaymentReconciliationInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PaymentReconciliationInvoice.business_id == business_id]

        if parent_id is not None:

            conditions.append(PaymentReconciliationInvoice.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PaymentReconciliationInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PaymentReconciliationInvoice)

            .where(*conditions)

            .order_by(PaymentReconciliationInvoice.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


