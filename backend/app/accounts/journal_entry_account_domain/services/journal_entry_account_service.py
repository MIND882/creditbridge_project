"""Read-only service for JournalEntryAccount; writes go through JournalEntry."""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.journal_entry_account_domain.models.journal_entry_account import JournalEntryAccount

from app.accounts.journal_entry_account_domain.repositories.journal_entry_account_repository import JournalEntryAccountRepository

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JournalEntryAccountService"]





class JournalEntryAccountService:

    def __init__(self, repository: Optional[JournalEntryAccountRepository] = None) -> None:

        self.repository = repository or JournalEntryAccountRepository()



    def get(self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID) -> JournalEntryAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("JournalEntryAccount", row_id)

        return row



    def list(self, db: Session, business_id: uuid.UUID, **filters: object) -> ResultPage[JournalEntryAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JournalEntryAccount].build(

            rows, total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
