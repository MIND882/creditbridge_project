"""Data access for OpeningInvoiceCreationToolItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.opening_invoice_creation_tool_item_domain.models.opening_invoice_creation_tool_item import OpeningInvoiceCreationToolItem

from app.core.pagination import normalise_paging



__all__ = ["OpeningInvoiceCreationToolItemRepository"]





class OpeningInvoiceCreationToolItemRepository:

    model = OpeningInvoiceCreationToolItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[OpeningInvoiceCreationToolItem]:

        return db.scalar(

            select(OpeningInvoiceCreationToolItem).where(

                OpeningInvoiceCreationToolItem.business_id == business_id, OpeningInvoiceCreationToolItem.id == row_id

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

    ) -> tuple[Sequence[OpeningInvoiceCreationToolItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [OpeningInvoiceCreationToolItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(OpeningInvoiceCreationToolItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(OpeningInvoiceCreationToolItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(OpeningInvoiceCreationToolItem)

            .where(*conditions)

            .order_by(OpeningInvoiceCreationToolItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


