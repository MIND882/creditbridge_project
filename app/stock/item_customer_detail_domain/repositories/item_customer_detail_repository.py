"""Data access for ItemCustomerDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_customer_detail_domain.models.item_customer_detail import ItemCustomerDetail

from app.core.pagination import normalise_paging



__all__ = ["ItemCustomerDetailRepository"]





class ItemCustomerDetailRepository:

    model = ItemCustomerDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ItemCustomerDetail]:

        return db.scalar(

            select(ItemCustomerDetail).where(

                ItemCustomerDetail.business_id == business_id, ItemCustomerDetail.id == row_id

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ItemCustomerDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ItemCustomerDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(ItemCustomerDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ItemCustomerDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ItemCustomerDetail)

            .where(*conditions)

            .order_by(ItemCustomerDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
