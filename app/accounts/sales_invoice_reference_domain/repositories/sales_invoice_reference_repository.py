"""Data access for SalesInvoiceReference. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.sales_invoice_reference_domain.models.sales_invoice_reference import SalesInvoiceReference

from app.core.pagination import normalise_paging



__all__ = ["SalesInvoiceReferenceRepository"]





class SalesInvoiceReferenceRepository:

    model = SalesInvoiceReference





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SalesInvoiceReference]:

        return db.scalar(

            select(SalesInvoiceReference).where(

                SalesInvoiceReference.business_id == business_id, SalesInvoiceReference.id == row_id

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

    ) -> tuple[Sequence[SalesInvoiceReference], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SalesInvoiceReference.business_id == business_id]

        if parent_id is not None:

            conditions.append(SalesInvoiceReference.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SalesInvoiceReference).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SalesInvoiceReference)

            .where(*conditions)

            .order_by(SalesInvoiceReference.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


