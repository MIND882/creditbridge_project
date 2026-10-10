"""Business logic for ItemReorder.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_reorder_domain.models.item_reorder import ItemReorder

from app.stock.item_reorder_domain.repositories.item_reorder_repository import (

    ItemReorderRepository,

)

from app.stock.item_reorder_domain.schemas.item_reorder import (

    ItemReorderCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemReorderService"]





class ItemReorderService:

    def __init__(self, repository: Optional[ItemReorderRepository] = None) -> None:

        self.repository = repository or ItemReorderRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemReorder:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Reorder", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemReorder]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemReorder].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
