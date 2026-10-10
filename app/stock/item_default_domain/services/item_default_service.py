"""Business logic for ItemDefault.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_default_domain.models.item_default import ItemDefault

from app.stock.item_default_domain.repositories.item_default_repository import (

    ItemDefaultRepository,

)

from app.stock.item_default_domain.schemas.item_default import (

    ItemDefaultCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemDefaultService"]





class ItemDefaultService:

    def __init__(self, repository: Optional[ItemDefaultRepository] = None) -> None:

        self.repository = repository or ItemDefaultRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemDefault:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Default", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemDefault]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemDefault].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
