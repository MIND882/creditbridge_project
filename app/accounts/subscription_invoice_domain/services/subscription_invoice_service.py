"""Business logic for SubscriptionInvoice.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.subscription_invoice_domain.models.subscription_invoice import SubscriptionInvoice

from app.accounts.subscription_invoice_domain.repositories.subscription_invoice_repository import (

    SubscriptionInvoiceRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubscriptionInvoiceService"]





class SubscriptionInvoiceService:

    def __init__(self, repository: Optional[SubscriptionInvoiceRepository] = None) -> None:

        self.repository = repository or SubscriptionInvoiceRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionInvoice:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Subscription Invoice", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SubscriptionInvoice]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SubscriptionInvoice].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
