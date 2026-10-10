"""Data access for SalesInvoiceAdvance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoiceAdvanceRepository"]





class SalesInvoiceAdvanceRepository:

    model = SalesInvoiceAdvance





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoiceAdvance]:

        return db.scalar(

            select(SalesInvoiceAdvance).where(

                SalesInvoiceAdvance.business_id == business_id, SalesInvoiceAdvance.id == row_id

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

    ) -> tuple[Sequence[SalesInvoiceAdvance], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoiceAdvance.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesInvoiceAdvance.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoiceAdvance).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoiceAdvance)

            .where(*conditions)

            .order_by(SalesInvoiceAdvance.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


