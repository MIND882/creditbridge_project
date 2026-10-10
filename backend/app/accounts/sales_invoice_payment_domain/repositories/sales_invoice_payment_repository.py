"""Data access for SalesInvoicePayment. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_payment_domain.models.sales_invoice_payment import SalesInvoicePayment

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoicePaymentRepository"]





class SalesInvoicePaymentRepository:

    model = SalesInvoicePayment





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoicePayment]:

        return db.scalar(

            select(SalesInvoicePayment).where(

                SalesInvoicePayment.business_id == business_id, SalesInvoicePayment.id == row_id

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

    ) -> tuple[Sequence[SalesInvoicePayment], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoicePayment.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesInvoicePayment.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoicePayment).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoicePayment)

            .where(*conditions)

            .order_by(SalesInvoicePayment.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


