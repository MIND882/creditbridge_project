"""Data access for CustomerCreditLimit. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.customer_credit_limit_domain.models.customer_credit_limit import CustomerCreditLimit

from app.core.pagination import normalise_paging



__all__ = ["CustomerCreditLimitRepository"]





class CustomerCreditLimitRepository:

    model = CustomerCreditLimit





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CustomerCreditLimit]:

        return db.scalar(

            select(CustomerCreditLimit).where(

                CustomerCreditLimit.business_id == business_id, CustomerCreditLimit.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CustomerCreditLimit]:

        return db.scalar(

            select(CustomerCreditLimit).where(

                CustomerCreditLimit.business_id == business_id, CustomerCreditLimit.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[CustomerCreditLimit], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CustomerCreditLimit.business_id == business_id]

        if parent_id is not None:

            conditions.append(CustomerCreditLimit.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CustomerCreditLimit).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CustomerCreditLimit)

            .where(*conditions)

            .order_by(CustomerCreditLimit.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
