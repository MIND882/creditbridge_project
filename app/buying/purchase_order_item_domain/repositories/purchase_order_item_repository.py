"""Data access for PurchaseOrderItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.purchase_order_item_domain.models.purchase_order_item import PurchaseOrderItem

from app.core.pagination import normalise_paging



__all__ = ["PurchaseOrderItemRepository"]





class PurchaseOrderItemRepository:

    model = PurchaseOrderItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PurchaseOrderItem]:

        return db.scalar(

            select(PurchaseOrderItem).where(

                PurchaseOrderItem.business_id == business_id, PurchaseOrderItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PurchaseOrderItem]:

        return db.scalar(

            select(PurchaseOrderItem).where(

                PurchaseOrderItem.business_id == business_id, PurchaseOrderItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[PurchaseOrderItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PurchaseOrderItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(PurchaseOrderItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PurchaseOrderItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PurchaseOrderItem)

            .where(*conditions)

            .order_by(PurchaseOrderItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
