"""Data access for POSInvoiceReference. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_invoice_reference_domain.models.pos_invoice_reference import POSInvoiceReference

from app.core.pagination import normalise_paging



__all__ = ["POSInvoiceReferenceRepository"]





class POSInvoiceReferenceRepository:

    model = POSInvoiceReference





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSInvoiceReference]:

        return db.scalar(

            select(POSInvoiceReference).where(

                POSInvoiceReference.business_id == business_id, POSInvoiceReference.id == row_id

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

    ) -> tuple[Sequence[POSInvoiceReference], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSInvoiceReference.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSInvoiceReference.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSInvoiceReference).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSInvoiceReference)

            .where(*conditions)

            .order_by(POSInvoiceReference.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


