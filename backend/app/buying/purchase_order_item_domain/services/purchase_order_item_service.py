"""Business logic for PurchaseOrderItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.purchase_order_item_domain.models.purchase_order_item import PurchaseOrderItem

from app.buying.purchase_order_item_domain.repositories.purchase_order_item_repository import (

    PurchaseOrderItemRepository,

)

from app.buying.purchase_order_item_domain.schemas.purchase_order_item import (

    PurchaseOrderItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PurchaseOrderItemService"]





class PurchaseOrderItemService:

    def __init__(self, repository: Optional[PurchaseOrderItemRepository] = None) -> None:

        self.repository = repository or PurchaseOrderItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseOrderItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Purchase Order Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseOrderItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseOrderItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
