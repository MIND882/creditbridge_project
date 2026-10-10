"""Read-only service for PaymentEntryReference; writes go through PaymentEntry."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.payment_entry_reference_domain.models.payment_entry_reference import PaymentEntryReference

from app.accounts.payment_entry_reference_domain.repositories.payment_entry_reference_repository import PaymentEntryReferenceRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PaymentEntryReferenceService"]





class PaymentEntryReferenceService:

    def __init__(self, repository: Optional[PaymentEntryReferenceRepository] = None) -> None:

        self.repository = repository or PaymentEntryReferenceRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> PaymentEntryReference:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("PaymentEntryReference", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[PaymentEntryReference]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PaymentEntryReference].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
