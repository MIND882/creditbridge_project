"""Business logic for ProductionPlanSalesOrder.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.production_plan_sales_order_domain.models.production_plan_sales_order import ProductionPlanSalesOrder

from app.manufacturing.production_plan_sales_order_domain.repositories.production_plan_sales_order_repository import (

    ProductionPlanSalesOrderRepository,

)

from app.manufacturing.production_plan_sales_order_domain.schemas.production_plan_sales_order import (

    ProductionPlanSalesOrderCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProductionPlanSalesOrderService"]





class ProductionPlanSalesOrderService:

    def __init__(self, repository: Optional[ProductionPlanSalesOrderRepository] = None) -> None:

        self.repository = repository or ProductionPlanSalesOrderRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProductionPlanSalesOrder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Production Plan Sales Order", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProductionPlanSalesOrder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProductionPlanSalesOrder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
