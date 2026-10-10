"""Business logic for ItemSupplier.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_supplier_domain.models.item_supplier import ItemSupplier

from app.stock.item_supplier_domain.repositories.item_supplier_repository import (

    ItemSupplierRepository,

)

from app.stock.item_supplier_domain.schemas.item_supplier import (

    ItemSupplierCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemSupplierService"]





class ItemSupplierService:

    def __init__(self, repository: Optional[ItemSupplierRepository] = None) -> None:

        self.repository = repository or ItemSupplierRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ItemSupplier:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Item Supplier", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ItemSupplier]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ItemSupplier].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
