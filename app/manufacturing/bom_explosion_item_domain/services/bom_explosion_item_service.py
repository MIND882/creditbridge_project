"""Business logic for BomExplosionItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_explosion_item_domain.models.bom_explosion_item import BomExplosionItem

from app.manufacturing.bom_explosion_item_domain.repositories.bom_explosion_item_repository import (

    BomExplosionItemRepository,

)

from app.manufacturing.bom_explosion_item_domain.schemas.bom_explosion_item import (

    BomExplosionItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomExplosionItemService"]





class BomExplosionItemService:

    def __init__(self, repository: Optional[BomExplosionItemRepository] = None) -> None:

        self.repository = repository or BomExplosionItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomExplosionItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Explosion Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomExplosionItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomExplosionItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
