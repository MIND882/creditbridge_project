"""Business logic for StockReconciliationItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.stock_reconciliation_item_domain.models.stock_reconciliation_item import StockReconciliationItem

from app.stock.stock_reconciliation_item_domain.repositories.stock_reconciliation_item_repository import (

    StockReconciliationItemRepository,

)

from app.stock.stock_reconciliation_item_domain.schemas.stock_reconciliation_item import (

    StockReconciliationItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["StockReconciliationItemService"]





class StockReconciliationItemService:

    def __init__(self, repository: Optional[StockReconciliationItemRepository] = None) -> None:

        self.repository = repository or StockReconciliationItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> StockReconciliationItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Stock Reconciliation Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[StockReconciliationItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[StockReconciliationItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
