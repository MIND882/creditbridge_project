"""Business logic for PaymentReconciliationPayment.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_reconciliation_payment_domain.models.payment_reconciliation_payment import PaymentReconciliationPayment

from app.accounts.payment_reconciliation_payment_domain.repositories.payment_reconciliation_payment_repository import (

    PaymentReconciliationPaymentRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentReconciliationPaymentService"]





class PaymentReconciliationPaymentService:

    def __init__(self, repository: Optional[PaymentReconciliationPaymentRepository] = None) -> None:

        self.repository = repository or PaymentReconciliationPaymentRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PaymentReconciliationPayment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Payment Reconciliation Payment", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PaymentReconciliationPayment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentReconciliationPayment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
