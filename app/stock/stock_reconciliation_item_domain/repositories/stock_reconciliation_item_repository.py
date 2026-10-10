"""Data access for StockReconciliationItem. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_reconciliation_item_domain.models.stock_reconciliation_item import StockReconciliationItem

from app.core.pagination import normalise_paging



__all__ = ["StockReconciliationItemRepository"]





class StockReconciliationItemRepository:

    model = StockReconciliationItem





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockReconciliationItem]:

        return db.scalar(

            select(StockReconciliationItem).where(

                StockReconciliationItem.business_id == business_id, StockReconciliationItem.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockReconciliationItem]:

        return db.scalar(

            select(StockReconciliationItem).where(

                StockReconciliationItem.business_id == business_id, StockReconciliationItem.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0, limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[StockReconciliationItem], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockReconciliationItem.business_id == business_id]

        if parent_id is not None:

            conditions.append(StockReconciliationItem.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(StockReconciliationItem).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockReconciliationItem)

            .where(*conditions)

            .order_by(StockReconciliationItem.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total
