"""Business logic for SalesForecastItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.sales_forecast_item_domain.models.sales_forecast_item import SalesForecastItem

from app.manufacturing.sales_forecast_item_domain.repositories.sales_forecast_item_repository import (

    SalesForecastItemRepository,

)

from app.manufacturing.sales_forecast_item_domain.schemas.sales_forecast_item import (

    SalesForecastItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesForecastItemService"]





class SalesForecastItemService:

    def __init__(self, repository: Optional[SalesForecastItemRepository] = None) -> None:

        self.repository = repository or SalesForecastItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesForecastItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Forecast Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesForecastItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesForecastItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
