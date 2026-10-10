"""Data access for QuickStockBalance. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.quick_stock_balance_domain.models.quick_stock_balance import QuickStockBalance

from app.core.pagination import normalise_paging



__all__ = ["QuickStockBalanceRepository"]





class QuickStockBalanceRepository:

    model = QuickStockBalance





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[QuickStockBalance]:

        return db.scalar(

            select(QuickStockBalance).where(

                QuickStockBalance.business_id == business_id

            )

        )



    def add(self, db: Session, row: QuickStockBalance) -> QuickStockBalance:

        db.add(row)

        db.flush()

        return row
