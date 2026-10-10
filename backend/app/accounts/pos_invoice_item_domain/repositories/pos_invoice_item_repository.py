"""Data access for POSInvoiceItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_invoice_item_domain.models.pos_invoice_item import POSInvoiceItem

from app.core.pagination import normalise_paging



__all__ = ["POSInvoiceItemRepository"]





class POSInvoiceItemRepository:

    model = POSInvoiceItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSInvoiceItem]:

        return db.scalar(

            select(POSInvoiceItem).where(

                POSInvoiceItem.business_id == business_id, POSInvoiceItem.id == row_id

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

    ) -> tuple[Sequence[POSInvoiceItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSInvoiceItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSInvoiceItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSInvoiceItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSInvoiceItem)

            .where(*conditions)

            .order_by(POSInvoiceItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


