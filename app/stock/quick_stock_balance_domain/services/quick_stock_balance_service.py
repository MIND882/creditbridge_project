"""Business logic for Quick Stock Balance -- port of

``erpnext/stock/doctype/quick_stock_balance/quick_stock_balance.py``.



Upstream has 1 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.quick_stock_balance_domain.models.quick_stock_balance import QuickStockBalance

from app.stock.quick_stock_balance_domain.repositories.quick_stock_balance_repository import (

    QuickStockBalanceRepository,

)

from app.stock.quick_stock_balance_domain.schemas.quick_stock_balance import (

    QuickStockBalanceUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["QuickStockBalanceService"]





class QuickStockBalanceService:

    def __init__(self, repository: Optional[QuickStockBalanceRepository] = None) -> None:

        self.repository = repository or QuickStockBalanceRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> QuickStockBalance:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = QuickStockBalance(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: QuickStockBalanceUpdate

    ) -> QuickStockBalance:

        row = self.get_or_create(db, business_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row

        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row
