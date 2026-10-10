"""Business logic for UnreconcilePaymentEntries.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.unreconcile_payment_entries_domain.models.unreconcile_payment_entries import UnreconcilePaymentEntries

from app.accounts.unreconcile_payment_entries_domain.repositories.unreconcile_payment_entries_repository import (

    UnreconcilePaymentEntriesRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["UnreconcilePaymentEntriesService"]





class UnreconcilePaymentEntriesService:

    def __init__(self, repository: Optional[UnreconcilePaymentEntriesRepository] = None) -> None:

        self.repository = repository or UnreconcilePaymentEntriesRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> UnreconcilePaymentEntries:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Unreconcile Payment Entries", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[UnreconcilePaymentEntries]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[UnreconcilePaymentEntries].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
