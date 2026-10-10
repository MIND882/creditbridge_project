"""Read-only service for PaymentEntryDeduction; writes go through PaymentEntry."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_entry_deduction_domain.models.payment_entry_deduction import PaymentEntryDeduction

from app.accounts.payment_entry_deduction_domain.repositories.payment_entry_deduction_repository import PaymentEntryDeductionRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentEntryDeductionService"]





class PaymentEntryDeductionService:

    def __init__(self, repository: Optional[PaymentEntryDeductionRepository] = None) -> None:

        self.repository = repository or PaymentEntryDeductionRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PaymentEntryDeduction:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("PaymentEntryDeduction", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PaymentEntryDeduction]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentEntryDeduction].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
