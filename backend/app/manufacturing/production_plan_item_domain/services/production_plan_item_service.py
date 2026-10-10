"""Business logic for ProductionPlanItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_item_domain.models.production_plan_item import ProductionPlanItem

from app.manufacturing.production_plan_item_domain.repositories.production_plan_item_repository import (

    ProductionPlanItemRepository,

)

from app.manufacturing.production_plan_item_domain.schemas.production_plan_item import (

    ProductionPlanItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanItemService"]





class ProductionPlanItemService:

    def __init__(self, repository: Optional[ProductionPlanItemRepository] = None) -> None:

        self.repository = repository or ProductionPlanItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
