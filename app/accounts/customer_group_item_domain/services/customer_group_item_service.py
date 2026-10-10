"""Business logic for CustomerGroupItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.customer_group_item_domain.models.customer_group_item import CustomerGroupItem

from app.accounts.customer_group_item_domain.repositories.customer_group_item_repository import (

    CustomerGroupItemRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CustomerGroupItemService"]





class CustomerGroupItemService:

    def __init__(self, repository: Optional[CustomerGroupItemRepository] = None) -> None:

        self.repository = repository or CustomerGroupItemRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> CustomerGroupItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Customer Group Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[CustomerGroupItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[CustomerGroupItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
