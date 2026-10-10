"""Business logic for ProformaInvoiceItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.proforma_invoice_item_domain.models.proforma_invoice_item import ProformaInvoiceItem

from app.selling.proforma_invoice_item_domain.repositories.proforma_invoice_item_repository import (

    ProformaInvoiceItemRepository,

)

from app.selling.proforma_invoice_item_domain.schemas.proforma_invoice_item import (

    ProformaInvoiceItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ProformaInvoiceItemService"]





class ProformaInvoiceItemService:

    def __init__(self, repository: Optional[ProformaInvoiceItemRepository] = None) -> None:

        self.repository = repository or ProformaInvoiceItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ProformaInvoiceItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Proforma Invoice Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ProformaInvoiceItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ProformaInvoiceItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
