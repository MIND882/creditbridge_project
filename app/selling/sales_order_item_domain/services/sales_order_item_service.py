"""Business logic for SalesOrderItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.sales_order_item_domain.models.sales_order_item import SalesOrderItem

from app.selling.sales_order_item_domain.repositories.sales_order_item_repository import (

    SalesOrderItemRepository,

)

from app.selling.sales_order_item_domain.schemas.sales_order_item import (

    SalesOrderItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesOrderItemService"]





class SalesOrderItemService:

    def __init__(self, repository: Optional[SalesOrderItemRepository] = None) -> None:

        self.repository = repository or SalesOrderItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesOrderItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Order Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesOrderItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesOrderItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
