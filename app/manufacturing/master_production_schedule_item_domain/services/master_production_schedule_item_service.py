"""Business logic for MasterProductionScheduleItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.master_production_schedule_item_domain.models.master_production_schedule_item import MasterProductionScheduleItem

from app.manufacturing.master_production_schedule_item_domain.repositories.master_production_schedule_item_repository import (

    MasterProductionScheduleItemRepository,

)

from app.manufacturing.master_production_schedule_item_domain.schemas.master_production_schedule_item import (

    MasterProductionScheduleItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["MasterProductionScheduleItemService"]





class MasterProductionScheduleItemService:

    def __init__(self, repository: Optional[MasterProductionScheduleItemRepository] = None) -> None:

        self.repository = repository or MasterProductionScheduleItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MasterProductionScheduleItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Master Production Schedule Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MasterProductionScheduleItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MasterProductionScheduleItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
