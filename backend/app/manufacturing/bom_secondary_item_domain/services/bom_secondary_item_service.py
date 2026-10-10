"""Business logic for BomSecondaryItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_secondary_item_domain.models.bom_secondary_item import BomSecondaryItem

from app.manufacturing.bom_secondary_item_domain.repositories.bom_secondary_item_repository import (

    BomSecondaryItemRepository,

)

from app.manufacturing.bom_secondary_item_domain.schemas.bom_secondary_item import (

    BomSecondaryItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomSecondaryItemService"]





class BomSecondaryItemService:

    def __init__(self, repository: Optional[BomSecondaryItemRepository] = None) -> None:

        self.repository = repository or BomSecondaryItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomSecondaryItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Secondary Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomSecondaryItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomSecondaryItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
