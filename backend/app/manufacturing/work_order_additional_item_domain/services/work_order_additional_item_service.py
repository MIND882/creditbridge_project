"""Business logic for WorkOrderAdditionalItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.work_order_additional_item_domain.models.work_order_additional_item import WorkOrderAdditionalItem

from app.manufacturing.work_order_additional_item_domain.repositories.work_order_additional_item_repository import (

    WorkOrderAdditionalItemRepository,

)

from app.manufacturing.work_order_additional_item_domain.schemas.work_order_additional_item import (

    WorkOrderAdditionalItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkOrderAdditionalItemService"]





class WorkOrderAdditionalItemService:

    def __init__(self, repository: Optional[WorkOrderAdditionalItemRepository] = None) -> None:

        self.repository = repository or WorkOrderAdditionalItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrderAdditionalItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Work Order Additional Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkOrderAdditionalItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkOrderAdditionalItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
