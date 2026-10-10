"""Data access for SupplierQuotation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_quotation_domain.models.supplier_quotation import SupplierQuotation

from app.core.pagination import normalise_paging



__all__ = ["SupplierQuotationRepository"]





class SupplierQuotationRepository:

    model = SupplierQuotation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierQuotation]:

        return db.scalar(

            select(SupplierQuotation).where(

                SupplierQuotation.business_id == business_id, SupplierQuotation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierQuotation]:

        return db.scalar(

            select(SupplierQuotation).where(

                SupplierQuotation.business_id == business_id, SupplierQuotation.name == name

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

    ) -> tuple[Sequence[SupplierQuotation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierQuotation.business_id == business_id]

        if not include_cancelled:

            conditions.append(SupplierQuotation.docstatus != 2)

        if search:

            conditions.append(SupplierQuotation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SupplierQuotation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierQuotation)

            .where(*conditions)

            .order_by(SupplierQuotation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SupplierQuotation) -> SupplierQuotation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SupplierQuotation) -> None:

        db.delete(row)

        db.flush()
