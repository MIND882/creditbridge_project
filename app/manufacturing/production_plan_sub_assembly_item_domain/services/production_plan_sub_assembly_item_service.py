"""Business logic for ProductionPlanSubAssemblyItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_sub_assembly_item_domain.models.production_plan_sub_assembly_item import ProductionPlanSubAssemblyItem

from app.manufacturing.production_plan_sub_assembly_item_domain.repositories.production_plan_sub_assembly_item_repository import (

    ProductionPlanSubAssemblyItemRepository,

)

from app.manufacturing.production_plan_sub_assembly_item_domain.schemas.production_plan_sub_assembly_item import (

    ProductionPlanSubAssemblyItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanSubAssemblyItemService"]





class ProductionPlanSubAssemblyItemService:

    def __init__(self, repository: Optional[ProductionPlanSubAssemblyItemRepository] = None) -> None:

        self.repository = repository or ProductionPlanSubAssemblyItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanSubAssemblyItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Sub Assembly Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanSubAssemblyItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanSubAssemblyItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
