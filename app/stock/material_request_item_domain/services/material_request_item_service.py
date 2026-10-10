"""Business logic for MaterialRequestItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.material_request_item_domain.models.material_request_item import MaterialRequestItem

from app.stock.material_request_item_domain.repositories.material_request_item_repository import (

    MaterialRequestItemRepository,

)

from app.stock.material_request_item_domain.schemas.material_request_item import (

    MaterialRequestItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["MaterialRequestItemService"]





class MaterialRequestItemService:

    def __init__(self, repository: Optional[MaterialRequestItemRepository] = None) -> None:

        self.repository = repository or MaterialRequestItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MaterialRequestItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Material Request Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MaterialRequestItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MaterialRequestItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
