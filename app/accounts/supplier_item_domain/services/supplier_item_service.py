"""Business logic for SupplierItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.supplier_item_domain.models.supplier_item import SupplierItem

from app.accounts.supplier_item_domain.repositories.supplier_item_repository import (

    SupplierItemRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierItemService"]





class SupplierItemService:

    def __init__(self, repository: Optional[SupplierItemRepository] = None) -> None:

        self.repository = repository or SupplierItemRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
