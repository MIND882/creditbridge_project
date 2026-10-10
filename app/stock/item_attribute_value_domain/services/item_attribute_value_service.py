"""Business logic for ItemAttributeValue.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_attribute_value_domain.models.item_attribute_value import ItemAttributeValue

from app.stock.item_attribute_value_domain.repositories.item_attribute_value_repository import (

    ItemAttributeValueRepository,

)

from app.stock.item_attribute_value_domain.schemas.item_attribute_value import (

    ItemAttributeValueCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemAttributeValueService"]





class ItemAttributeValueService:

    def __init__(self, repository: Optional[ItemAttributeValueRepository] = None) -> None:

        self.repository = repository or ItemAttributeValueRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemAttributeValue:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Attribute Value", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemAttributeValue]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemAttributeValue].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
