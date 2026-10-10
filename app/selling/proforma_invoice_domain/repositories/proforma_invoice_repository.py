"""Data access for ProformaInvoice. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.proforma_invoice_domain.models.proforma_invoice import ProformaInvoice

from app.core.pagination import normalise_paging



__all__ = ["ProformaInvoiceRepository"]





class ProformaInvoiceRepository:

    model = ProformaInvoice





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ProformaInvoice]:

        return db.scalar(

            select(ProformaInvoice).where(

                ProformaInvoice.business_id == business_id, ProformaInvoice.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ProformaInvoice]:

        return db.scalar(

            select(ProformaInvoice).where(

                ProformaInvoice.business_id == business_id, ProformaInvoice.name == name

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

    ) -> tuple[Sequence[ProformaInvoice], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ProformaInvoice.business_id == business_id]

        if search:

            conditions.append(ProformaInvoice.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ProformaInvoice).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ProformaInvoice)

            .where(*conditions)

            .order_by(ProformaInvoice.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: ProformaInvoice) -> ProformaInvoice:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ProformaInvoice) -> None:

        db.delete(row)

        db.flush()
