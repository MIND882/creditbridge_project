"""Data access for RequestForQuotationItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.request_for_quotation_item_domain.models.request_for_quotation_item import RequestForQuotationItem

from app.core.pagination import normalise_paging



__all__ = ["RequestForQuotationItemRepository"]





class RequestForQuotationItemRepository:

    model = RequestForQuotationItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RequestForQuotationItem]:

        return db.scalar(

            select(RequestForQuotationItem).where(

                RequestForQuotationItem.business_id == business_id, RequestForQuotationItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[RequestForQuotationItem]:

        return db.scalar(

            select(RequestForQuotationItem).where(

                RequestForQuotationItem.business_id == business_id, RequestForQuotationItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[RequestForQuotationItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RequestForQuotationItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(RequestForQuotationItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(RequestForQuotationItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RequestForQuotationItem)

            .where(*conditions)

            .order_by(RequestForQuotationItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
