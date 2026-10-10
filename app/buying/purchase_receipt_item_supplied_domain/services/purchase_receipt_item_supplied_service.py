"""Business logic for PurchaseReceiptItemSupplied.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.purchase_receipt_item_supplied_domain.models.purchase_receipt_item_supplied import PurchaseReceiptItemSupplied

from app.buying.purchase_receipt_item_supplied_domain.repositories.purchase_receipt_item_supplied_repository import (

    PurchaseReceiptItemSuppliedRepository,

)

from app.buying.purchase_receipt_item_supplied_domain.schemas.purchase_receipt_item_supplied import (

    PurchaseReceiptItemSuppliedCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PurchaseReceiptItemSuppliedService"]





class PurchaseReceiptItemSuppliedService:

    def __init__(self, repository: Optional[PurchaseReceiptItemSuppliedRepository] = None) -> None:

        self.repository = repository or PurchaseReceiptItemSuppliedRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseReceiptItemSupplied:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Purchase Receipt Item Supplied", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseReceiptItemSupplied]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseReceiptItemSupplied].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
