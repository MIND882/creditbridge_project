"""Business logic for WorkOrderItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.work_order_item_domain.models.work_order_item import WorkOrderItem

from app.manufacturing.work_order_item_domain.repositories.work_order_item_repository import (

    WorkOrderItemRepository,

)

from app.manufacturing.work_order_item_domain.schemas.work_order_item import (

    WorkOrderItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkOrderItemService"]





class WorkOrderItemService:

    def __init__(self, repository: Optional[WorkOrderItemRepository] = None) -> None:

        self.repository = repository or WorkOrderItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrderItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Work Order Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkOrderItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkOrderItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
