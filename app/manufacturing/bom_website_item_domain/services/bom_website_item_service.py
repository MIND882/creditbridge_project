"""Business logic for BomWebsiteItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_website_item_domain.models.bom_website_item import BomWebsiteItem

from app.manufacturing.bom_website_item_domain.repositories.bom_website_item_repository import (

    BomWebsiteItemRepository,

)

from app.manufacturing.bom_website_item_domain.schemas.bom_website_item import (

    BomWebsiteItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomWebsiteItemService"]





class BomWebsiteItemService:

    def __init__(self, repository: Optional[BomWebsiteItemRepository] = None) -> None:

        self.repository = repository or BomWebsiteItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomWebsiteItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Website Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomWebsiteItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomWebsiteItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
