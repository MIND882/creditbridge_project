"""Business logic for RepostAccountingLedgerItems.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.repost_accounting_ledger_items_domain.models.repost_accounting_ledger_items import RepostAccountingLedgerItems

from app.accounts.repost_accounting_ledger_items_domain.repositories.repost_accounting_ledger_items_repository import (

    RepostAccountingLedgerItemsRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["RepostAccountingLedgerItemsService"]





class RepostAccountingLedgerItemsService:

    def __init__(self, repository: Optional[RepostAccountingLedgerItemsRepository] = None) -> None:

        self.repository = repository or RepostAccountingLedgerItemsRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> RepostAccountingLedgerItems:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Repost Accounting Ledger Items", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[RepostAccountingLedgerItems]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[RepostAccountingLedgerItems].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
