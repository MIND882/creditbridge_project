"""Business logic for ProductionPlanMaterialRequest.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_material_request_domain.models.production_plan_material_request import ProductionPlanMaterialRequest

from app.manufacturing.production_plan_material_request_domain.repositories.production_plan_material_request_repository import (

    ProductionPlanMaterialRequestRepository,

)

from app.manufacturing.production_plan_material_request_domain.schemas.production_plan_material_request import (

    ProductionPlanMaterialRequestCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanMaterialRequestService"]





class ProductionPlanMaterialRequestService:

    def __init__(self, repository: Optional[ProductionPlanMaterialRequestRepository] = None) -> None:

        self.repository = repository or ProductionPlanMaterialRequestRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanMaterialRequest:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Material Request", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanMaterialRequest]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanMaterialRequest].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
