"""Business logic for OpeningInvoiceCreationToolItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.opening_invoice_creation_tool_item_domain.models.opening_invoice_creation_tool_item import OpeningInvoiceCreationToolItem

from app.accounts.opening_invoice_creation_tool_item_domain.repositories.opening_invoice_creation_tool_item_repository import (

    OpeningInvoiceCreationToolItemRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["OpeningInvoiceCreationToolItemService"]





class OpeningInvoiceCreationToolItemService:

    def __init__(self, repository: Optional[OpeningInvoiceCreationToolItemRepository] = None) -> None:

        self.repository = repository or OpeningInvoiceCreationToolItemRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> OpeningInvoiceCreationToolItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Opening Invoice Creation Tool Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[OpeningInvoiceCreationToolItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[OpeningInvoiceCreationToolItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
