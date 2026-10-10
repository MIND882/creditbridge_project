"""Business logic for LandedCostItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.landed_cost_item_domain.models.landed_cost_item import LandedCostItem

from app.stock.landed_cost_item_domain.repositories.landed_cost_item_repository import (

    LandedCostItemRepository,

)

from app.stock.landed_cost_item_domain.schemas.landed_cost_item import (

    LandedCostItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["LandedCostItemService"]





class LandedCostItemService:

    def __init__(self, repository: Optional[LandedCostItemRepository] = None) -> None:

        self.repository = repository or LandedCostItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> LandedCostItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Landed Cost Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[LandedCostItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[LandedCostItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
