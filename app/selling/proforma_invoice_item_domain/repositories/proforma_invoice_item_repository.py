"""Data access for ProformaInvoiceItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.proforma_invoice_item_domain.models.proforma_invoice_item import ProformaInvoiceItem

from app.core.pagination import normalise_paging



__all__ = ["ProformaInvoiceItemRepository"]





class ProformaInvoiceItemRepository:

    model = ProformaInvoiceItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProformaInvoiceItem]:

        return db.scalar(

            select(ProformaInvoiceItem).where(

                ProformaInvoiceItem.business_id == business_id, ProformaInvoiceItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProformaInvoiceItem]:

        return db.scalar(

            select(ProformaInvoiceItem).where(

                ProformaInvoiceItem.business_id == business_id, ProformaInvoiceItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ProformaInvoiceItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProformaInvoiceItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(ProformaInvoiceItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ProformaInvoiceItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProformaInvoiceItem)

            .where(*conditions)

            .order_by(ProformaInvoiceItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
