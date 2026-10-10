"""Business logic for SalesInvoiceReference.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.sales_invoice_reference_domain.models.sales_invoice_reference import SalesInvoiceReference

from app.accounts.sales_invoice_reference_domain.repositories.sales_invoice_reference_repository import (

    SalesInvoiceReferenceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesInvoiceReferenceService"]





class SalesInvoiceReferenceService:

    def __init__(self, repository: Optional[SalesInvoiceReferenceRepository] = None) -> None:

        self.repository = repository or SalesInvoiceReferenceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoiceReference:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Invoice Reference", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesInvoiceReference]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesInvoiceReference].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
