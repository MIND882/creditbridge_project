"""Data access for CustomerNumberAtSupplier. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.customer_number_at_supplier_domain.models.customer_number_at_supplier import CustomerNumberAtSupplier

from app.core.pagination import normalise_paging



__all__ = ["CustomerNumberAtSupplierRepository"]





class CustomerNumberAtSupplierRepository:

    model = CustomerNumberAtSupplier





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CustomerNumberAtSupplier]:

        return db.scalar(

            select(CustomerNumberAtSupplier).where(

                CustomerNumberAtSupplier.business_id == business_id, CustomerNumberAtSupplier.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CustomerNumberAtSupplier]:

        return db.scalar(

            select(CustomerNumberAtSupplier).where(

                CustomerNumberAtSupplier.business_id == business_id, CustomerNumberAtSupplier.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[CustomerNumberAtSupplier], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CustomerNumberAtSupplier.business_id == business_id]

        if parent_id is not None:

            conditions.append(CustomerNumberAtSupplier.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CustomerNumberAtSupplier).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CustomerNumberAtSupplier)

            .where(*conditions)

            .order_by(CustomerNumberAtSupplier.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
