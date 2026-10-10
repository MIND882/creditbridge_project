"""Data access for RequestForQuotationSupplier. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.request_for_quotation_supplier_domain.models.request_for_quotation_supplier import RequestForQuotationSupplier

from app.core.pagination import normalise_paging



__all__ = ["RequestForQuotationSupplierRepository"]





class RequestForQuotationSupplierRepository:

    model = RequestForQuotationSupplier





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RequestForQuotationSupplier]:

        return db.scalar(

            select(RequestForQuotationSupplier).where(

                RequestForQuotationSupplier.business_id == business_id, RequestForQuotationSupplier.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[RequestForQuotationSupplier]:

        return db.scalar(

            select(RequestForQuotationSupplier).where(

                RequestForQuotationSupplier.business_id == business_id, RequestForQuotationSupplier.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[RequestForQuotationSupplier], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RequestForQuotationSupplier.business_id == business_id]

        if parent_id is not None:

            conditions.append(RequestForQuotationSupplier.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(RequestForQuotationSupplier).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RequestForQuotationSupplier)

            .where(*conditions)

            .order_by(RequestForQuotationSupplier.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
