"""Data access for POSCustomerGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pos_customer_group_domain.models.pos_customer_group import POSCustomerGroup

from app.core.pagination import normalise_paging



__all__ = ["POSCustomerGroupRepository"]





class POSCustomerGroupRepository:

    model = POSCustomerGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[POSCustomerGroup]:

        return db.scalar(

            select(POSCustomerGroup).where(

                POSCustomerGroup.business_id == business_id, POSCustomerGroup.id == row_id

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

    ) -> tuple[Sequence[POSCustomerGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [POSCustomerGroup.business_id == business_id]

        if parent_id is not None:

            conditions.append(POSCustomerGroup.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(POSCustomerGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(POSCustomerGroup)

            .where(*conditions)

            .order_by(POSCustomerGroup.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


