"""Business logic for DeliveryNoteItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.delivery_note_item_domain.models.delivery_note_item import DeliveryNoteItem

from app.stock.delivery_note_item_domain.repositories.delivery_note_item_repository import (

    DeliveryNoteItemRepository,

)

from app.stock.delivery_note_item_domain.schemas.delivery_note_item import (

    DeliveryNoteItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DeliveryNoteItemService"]





class DeliveryNoteItemService:

    def __init__(self, repository: Optional[DeliveryNoteItemRepository] = None) -> None:

        self.repository = repository or DeliveryNoteItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DeliveryNoteItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Delivery Note Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DeliveryNoteItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DeliveryNoteItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
