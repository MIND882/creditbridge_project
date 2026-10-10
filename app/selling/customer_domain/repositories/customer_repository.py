"""Data access for Customer. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.customer_domain.models.customer import Customer

from app.core.pagination import normalise_paging



__all__ = ["CustomerRepository"]





class CustomerRepository:

    model = Customer





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Customer]:

        return db.scalar(

            select(Customer).where(

                Customer.business_id == business_id, Customer.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Customer]:

        return db.scalar(

            select(Customer).where(

                Customer.business_id == business_id, Customer.name == name

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

    ) -> tuple[Sequence[Customer], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Customer.business_id == business_id]

        if search:

            conditions.append(Customer.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Customer).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Customer)

            .where(*conditions)

            .order_by(Customer.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: Customer) -> Customer:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Customer) -> None:

        db.delete(row)

        db.flush()
