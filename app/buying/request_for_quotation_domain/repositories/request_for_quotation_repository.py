"""Data access for RequestForQuotation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.request_for_quotation_domain.models.request_for_quotation import RequestForQuotation

from app.core.pagination import normalise_paging



__all__ = ["RequestForQuotationRepository"]





class RequestForQuotationRepository:

    model = RequestForQuotation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[RequestForQuotation]:

        return db.scalar(

            select(RequestForQuotation).where(

                RequestForQuotation.business_id == business_id, RequestForQuotation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[RequestForQuotation]:

        return db.scalar(

            select(RequestForQuotation).where(

                RequestForQuotation.business_id == business_id, RequestForQuotation.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

        include_cancelled: bool = False,

    ) -> tuple[Sequence[RequestForQuotation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [RequestForQuotation.business_id == business_id]

        if not include_cancelled:

            conditions.append(RequestForQuotation.docstatus != 2)

        if search:

            conditions.append(RequestForQuotation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(RequestForQuotation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(RequestForQuotation)

            .where(*conditions)

            .order_by(RequestForQuotation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: RequestForQuotation) -> RequestForQuotation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: RequestForQuotation) -> None:

        db.delete(row)

        db.flush()
