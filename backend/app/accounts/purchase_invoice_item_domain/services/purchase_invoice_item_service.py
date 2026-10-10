"""Business logic for PurchaseInvoiceItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.purchase_invoice_item_domain.models.purchase_invoice_item import PurchaseInvoiceItem

from app.accounts.purchase_invoice_item_domain.repositories.purchase_invoice_item_repository import (

    PurchaseInvoiceItemRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PurchaseInvoiceItemService"]





class PurchaseInvoiceItemService:

    def __init__(self, repository: Optional[PurchaseInvoiceItemRepository] = None) -> None:

        self.repository = repository or PurchaseInvoiceItemRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PurchaseInvoiceItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Purchase Invoice Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PurchaseInvoiceItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PurchaseInvoiceItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
