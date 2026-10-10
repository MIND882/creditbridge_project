"""Data access for Quotation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.quotation_domain.models.quotation import Quotation

from app.core.pagination import normalise_paging



__all__ = ["QuotationRepository"]





class QuotationRepository:

    model = Quotation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Quotation]:

        return db.scalar(

            select(Quotation).where(

                Quotation.business_id == business_id, Quotation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Quotation]:

        return db.scalar(

            select(Quotation).where(

                Quotation.business_id == business_id, Quotation.name == name

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

    ) -> tuple[Sequence[Quotation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Quotation.business_id == business_id]

        if not include_cancelled:

            conditions.append(Quotation.docstatus != 2)

        if search:

            conditions.append(Quotation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Quotation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Quotation)

            .where(*conditions)

            .order_by(Quotation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Quotation) -> Quotation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Quotation) -> None:

        db.delete(row)

        db.flush()
