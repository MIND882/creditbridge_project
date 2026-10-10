"""Business logic for RepostPaymentLedgerItems.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.repost_payment_ledger_items_domain.models.repost_payment_ledger_items import RepostPaymentLedgerItems

from app.accounts.repost_payment_ledger_items_domain.repositories.repost_payment_ledger_items_repository import (

    RepostPaymentLedgerItemsRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RepostPaymentLedgerItemsService"]





class RepostPaymentLedgerItemsService:

    def __init__(self, repository: Optional[RepostPaymentLedgerItemsRepository] = None) -> None:

        self.repository = repository or RepostPaymentLedgerItemsRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostPaymentLedgerItems:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Payment Ledger Items", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostPaymentLedgerItems]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostPaymentLedgerItems].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
