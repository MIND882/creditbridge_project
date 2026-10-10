"""Business logic for ProductionPlanMaterialRequestWarehouse.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_material_request_warehouse_domain.models.production_plan_material_request_warehouse import ProductionPlanMaterialRequestWarehouse

from app.manufacturing.production_plan_material_request_warehouse_domain.repositories.production_plan_material_request_warehouse_repository import (

    ProductionPlanMaterialRequestWarehouseRepository,

)

from app.manufacturing.production_plan_material_request_warehouse_domain.schemas.production_plan_material_request_warehouse import (

    ProductionPlanMaterialRequestWarehouseCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanMaterialRequestWarehouseService"]





class ProductionPlanMaterialRequestWarehouseService:

    def __init__(self, repository: Optional[ProductionPlanMaterialRequestWarehouseRepository] = None) -> None:

        self.repository = repository or ProductionPlanMaterialRequestWarehouseRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanMaterialRequestWarehouse:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Material Request Warehouse", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanMaterialRequestWarehouse]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanMaterialRequestWarehouse].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
