"""Data access for CustomerItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.customer_item_domain.models.customer_item import CustomerItem

from app.core.pagination import normalise_paging



__all__ = ["CustomerItemRepository"]





class CustomerItemRepository:

    model = CustomerItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CustomerItem]:

        return db.scalar(

            select(CustomerItem).where(

                CustomerItem.business_id == business_id, CustomerItem.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[CustomerItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CustomerItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(CustomerItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CustomerItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CustomerItem)

            .where(*conditions)

            .order_by(CustomerItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


