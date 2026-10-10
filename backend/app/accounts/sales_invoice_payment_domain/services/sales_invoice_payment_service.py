"""Business logic for SalesInvoicePayment.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.sales_invoice_payment_domain.models.sales_invoice_payment import SalesInvoicePayment

from app.accounts.sales_invoice_payment_domain.repositories.sales_invoice_payment_repository import (

    SalesInvoicePaymentRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesInvoicePaymentService"]





class SalesInvoicePaymentService:

    def __init__(self, repository: Optional[SalesInvoicePaymentRepository] = None) -> None:

        self.repository = repository or SalesInvoicePaymentRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesInvoicePayment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Invoice Payment", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesInvoicePayment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesInvoicePayment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
