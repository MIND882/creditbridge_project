"""Read-only service for BankTransactionPayment; writes go through BankTransaction."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.bank_transaction_payments_domain.models.bank_transaction_payments import BankTransactionPayment

from app.accounts.bank_transaction_payments_domain.repositories.bank_transaction_payments_repository import BankTransactionPaymentRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BankTransactionPaymentService"]





class BankTransactionPaymentService:

    def __init__(self, repository: Optional[BankTransactionPaymentRepository] = None) -> None:

        self.repository = repository or BankTransactionPaymentRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> BankTransactionPayment:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BankTransactionPayment", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[BankTransactionPayment]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BankTransactionPayment].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
