"""Business logic for BomCreatorItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_creator_item_domain.models.bom_creator_item import BomCreatorItem

from app.manufacturing.bom_creator_item_domain.repositories.bom_creator_item_repository import (

    BomCreatorItemRepository,

)

from app.manufacturing.bom_creator_item_domain.schemas.bom_creator_item import (

    BomCreatorItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomCreatorItemService"]





class BomCreatorItemService:

    def __init__(self, repository: Optional[BomCreatorItemRepository] = None) -> None:

        self.repository = repository or BomCreatorItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomCreatorItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Creator Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomCreatorItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomCreatorItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
