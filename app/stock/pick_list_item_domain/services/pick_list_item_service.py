"""Business logic for PickListItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.pick_list_item_domain.models.pick_list_item import PickListItem

from app.stock.pick_list_item_domain.repositories.pick_list_item_repository import (

    PickListItemRepository,

)

from app.stock.pick_list_item_domain.schemas.pick_list_item import (

    PickListItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PickListItemService"]





class PickListItemService:

    def __init__(self, repository: Optional[PickListItemRepository] = None) -> None:

        self.repository = repository or PickListItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PickListItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pick List Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PickListItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PickListItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
