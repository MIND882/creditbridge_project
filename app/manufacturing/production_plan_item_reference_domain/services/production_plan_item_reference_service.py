"""Business logic for ProductionPlanItemReference.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_item_reference_domain.models.production_plan_item_reference import ProductionPlanItemReference

from app.manufacturing.production_plan_item_reference_domain.repositories.production_plan_item_reference_repository import (

    ProductionPlanItemReferenceRepository,

)

from app.manufacturing.production_plan_item_reference_domain.schemas.production_plan_item_reference import (

    ProductionPlanItemReferenceCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanItemReferenceService"]





class ProductionPlanItemReferenceService:

    def __init__(self, repository: Optional[ProductionPlanItemReferenceRepository] = None) -> None:

        self.repository = repository or ProductionPlanItemReferenceRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanItemReference:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Item Reference", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanItemReference]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanItemReference].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
