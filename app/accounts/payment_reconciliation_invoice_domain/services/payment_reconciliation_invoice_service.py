"""Business logic for PaymentReconciliationInvoice.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_reconciliation_invoice_domain.models.payment_reconciliation_invoice import PaymentReconciliationInvoice

from app.accounts.payment_reconciliation_invoice_domain.repositories.payment_reconciliation_invoice_repository import (

    PaymentReconciliationInvoiceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentReconciliationInvoiceService"]





class PaymentReconciliationInvoiceService:

    def __init__(self, repository: Optional[PaymentReconciliationInvoiceRepository] = None) -> None:

        self.repository = repository or PaymentReconciliationInvoiceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentReconciliationInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Reconciliation Invoice", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentReconciliationInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentReconciliationInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
