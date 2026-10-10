"""Business logic for BlanketOrderItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.blanket_order_item_domain.models.blanket_order_item import BlanketOrderItem

from app.manufacturing.blanket_order_item_domain.repositories.blanket_order_item_repository import (

    BlanketOrderItemRepository,

)

from app.manufacturing.blanket_order_item_domain.schemas.blanket_order_item import (

    BlanketOrderItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BlanketOrderItemService"]





class BlanketOrderItemService:

    def __init__(self, repository: Optional[BlanketOrderItemRepository] = None) -> None:

        self.repository = repository or BlanketOrderItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BlanketOrderItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Blanket Order Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BlanketOrderItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BlanketOrderItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
