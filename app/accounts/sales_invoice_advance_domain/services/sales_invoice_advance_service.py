"""Business logic for SalesInvoiceAdvance.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.sales_invoice_advance_domain.models.sales_invoice_advance import SalesInvoiceAdvance

from app.accounts.sales_invoice_advance_domain.repositories.sales_invoice_advance_repository import (

    SalesInvoiceAdvanceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesInvoiceAdvanceService"]





class SalesInvoiceAdvanceService:

    def __init__(self, repository: Optional[SalesInvoiceAdvanceRepository] = None) -> None:

        self.repository = repository or SalesInvoiceAdvanceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoiceAdvance:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Invoice Advance", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesInvoiceAdvance]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesInvoiceAdvance].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
