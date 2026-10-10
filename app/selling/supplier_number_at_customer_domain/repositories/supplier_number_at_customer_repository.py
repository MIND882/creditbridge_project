"""Data access for SupplierNumberAtCustomer. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.supplier_number_at_customer_domain.models.supplier_number_at_customer import SupplierNumberAtCustomer

from app.core.pagination import normalise_paging



__all__ = ["SupplierNumberAtCustomerRepository"]





class SupplierNumberAtCustomerRepository:

    model = SupplierNumberAtCustomer





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SupplierNumberAtCustomer]:

        return db.scalar(

            select(SupplierNumberAtCustomer).where(

                SupplierNumberAtCustomer.business_id == business_id, SupplierNumberAtCustomer.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SupplierNumberAtCustomer]:

        return db.scalar(

            select(SupplierNumberAtCustomer).where(

                SupplierNumberAtCustomer.business_id == business_id, SupplierNumberAtCustomer.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[SupplierNumberAtCustomer], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SupplierNumberAtCustomer.business_id == business_id]

        if parent_id is not None:

            conditions.append(SupplierNumberAtCustomer.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SupplierNumberAtCustomer).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SupplierNumberAtCustomer)

            .where(*conditions)

            .order_by(SupplierNumberAtCustomer.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
