"""Data access for PurchaseInvoiceAdvance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.purchase_invoice_advance_domain.models.purchase_invoice_advance import PurchaseInvoiceAdvance

from app.core.pagination import normalise_paging



__all__ = ["PurchaseInvoiceAdvanceRepository"]





class PurchaseInvoiceAdvanceRepository:

    model = PurchaseInvoiceAdvance





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseInvoiceAdvance]:

        return db.scalar(

            select(PurchaseInvoiceAdvance).where(

                PurchaseInvoiceAdvance.business_id == business_id, PurchaseInvoiceAdvance.id == row_id

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

    ) -> tuple[Sequence[PurchaseInvoiceAdvance], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseInvoiceAdvance.business_id == business_id]

        if parent_id is not None:

            conditions.append(PurchaseInvoiceAdvance.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseInvoiceAdvance).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseInvoiceAdvance)

            .where(*conditions)

            .order_by(PurchaseInvoiceAdvance.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


