"""Data access for Supplier. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.supplier_domain.models.supplier import Supplier

from app.core.pagination import normalise_paging



__all__ = ["SupplierRepository"]





class SupplierRepository:

    model = Supplier





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Supplier]:

        return db.scalar(

            select(Supplier).where(

                Supplier.business_id == business_id, Supplier.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Supplier]:

        return db.scalar(

            select(Supplier).where(

                Supplier.business_id == business_id, Supplier.name == name

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

    ) -> tuple[Sequence[Supplier], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Supplier.business_id == business_id]

        if search:

            conditions.append(Supplier.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Supplier).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Supplier)

            .where(*conditions)

            .order_by(Supplier.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Supplier) -> Supplier:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Supplier) -> None:

        db.delete(row)

        db.flush()
