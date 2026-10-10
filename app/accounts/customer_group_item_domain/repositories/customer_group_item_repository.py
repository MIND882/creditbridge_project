"""Data access for CustomerGroupItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.customer_group_item_domain.models.customer_group_item import CustomerGroupItem

from app.core.pagination import normalise_paging



__all__ = ["CustomerGroupItemRepository"]





class CustomerGroupItemRepository:

    model = CustomerGroupItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CustomerGroupItem]:

        return db.scalar(

            select(CustomerGroupItem).where(

                CustomerGroupItem.business_id == business_id, CustomerGroupItem.id == row_id

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

    ) -> tuple[Sequence[CustomerGroupItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CustomerGroupItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(CustomerGroupItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CustomerGroupItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CustomerGroupItem)

            .where(*conditions)

            .order_by(CustomerGroupItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


