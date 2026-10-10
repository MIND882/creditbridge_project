"""Data access for SubscriptionInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_invoice_domain.models.subscription_invoice import SubscriptionInvoice

from app.core.pagination import normalise_paging



__all__ = ["SubscriptionInvoiceRepository"]





class SubscriptionInvoiceRepository:

    model = SubscriptionInvoice





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SubscriptionInvoice]:

        return db.scalar(

            select(SubscriptionInvoice).where(

                SubscriptionInvoice.business_id == business_id, SubscriptionInvoice.id == row_id

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

    ) -> tuple[Sequence[SubscriptionInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SubscriptionInvoice.business_id == business_id]

        if parent_id is not None:

            conditions.append(SubscriptionInvoice.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SubscriptionInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SubscriptionInvoice)

            .where(*conditions)

            .order_by(SubscriptionInvoice.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


