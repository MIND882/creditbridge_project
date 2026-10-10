"""Business logic for DiscountedInvoice.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.discounted_invoice_domain.models.discounted_invoice import DiscountedInvoice

from app.accounts.discounted_invoice_domain.repositories.discounted_invoice_repository import (

    DiscountedInvoiceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DiscountedInvoiceService"]





class DiscountedInvoiceService:

    def __init__(self, repository: Optional[DiscountedInvoiceRepository] = None) -> None:

        self.repository = repository or DiscountedInvoiceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> DiscountedInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Discounted Invoice", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[DiscountedInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[DiscountedInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
