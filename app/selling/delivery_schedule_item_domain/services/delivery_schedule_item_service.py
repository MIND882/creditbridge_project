"""Business logic for DeliveryScheduleItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.delivery_schedule_item_domain.models.delivery_schedule_item import DeliveryScheduleItem

from app.selling.delivery_schedule_item_domain.repositories.delivery_schedule_item_repository import (

    DeliveryScheduleItemRepository,

)

from app.selling.delivery_schedule_item_domain.schemas.delivery_schedule_item import (

    DeliveryScheduleItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DeliveryScheduleItemService"]





class DeliveryScheduleItemService:

    def __init__(self, repository: Optional[DeliveryScheduleItemRepository] = None) -> None:

        self.repository = repository or DeliveryScheduleItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryScheduleItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Delivery Schedule Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DeliveryScheduleItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DeliveryScheduleItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
