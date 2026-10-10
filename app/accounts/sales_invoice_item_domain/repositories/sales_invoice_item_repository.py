"""Data access for SalesInvoiceItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_item_domain.models.sales_invoice_item import SalesInvoiceItem

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoiceItemRepository"]





class SalesInvoiceItemRepository:

    model = SalesInvoiceItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoiceItem]:

        return db.scalar(

            select(SalesInvoiceItem).where(

                SalesInvoiceItem.business_id == business_id, SalesInvoiceItem.id == row_id

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

    ) -> tuple[Sequence[SalesInvoiceItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoiceItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesInvoiceItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoiceItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoiceItem)

            .where(*conditions)

            .order_by(SalesInvoiceItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


