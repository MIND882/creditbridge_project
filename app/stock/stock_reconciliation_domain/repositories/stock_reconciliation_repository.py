"""Data access for StockReconciliation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_reconciliation_domain.models.stock_reconciliation import StockReconciliation

from app.core.pagination import normalise_paging



__all__ = ["StockReconciliationRepository"]





class StockReconciliationRepository:

    model = StockReconciliation





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[StockReconciliation]:

        return db.scalar(

            select(StockReconciliation).where(

                StockReconciliation.business_id == business_id, StockReconciliation.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[StockReconciliation]:

        return db.scalar(

            select(StockReconciliation).where(

                StockReconciliation.business_id == business_id, StockReconciliation.name == name

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

    ) -> tuple[Sequence[StockReconciliation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [StockReconciliation.business_id == business_id]

        if not include_cancelled:

            conditions.append(StockReconciliation.docstatus != 2)

        if search:

            conditions.append(StockReconciliation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(StockReconciliation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(StockReconciliation)

            .where(*conditions)

            .order_by(StockReconciliation.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: StockReconciliation) -> StockReconciliation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: StockReconciliation) -> None:

        db.delete(row)

        db.flush()
