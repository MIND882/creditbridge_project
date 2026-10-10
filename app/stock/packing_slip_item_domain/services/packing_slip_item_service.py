"""Business logic for PackingSlipItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.packing_slip_item_domain.models.packing_slip_item import PackingSlipItem

from app.stock.packing_slip_item_domain.repositories.packing_slip_item_repository import (

    PackingSlipItemRepository,

)

from app.stock.packing_slip_item_domain.schemas.packing_slip_item import (

    PackingSlipItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PackingSlipItemService"]





class PackingSlipItemService:

    def __init__(self, repository: Optional[PackingSlipItemRepository] = None) -> None:

        self.repository = repository or PackingSlipItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PackingSlipItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Packing Slip Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PackingSlipItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PackingSlipItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
