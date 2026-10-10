"""Business logic for JournalEntryTemplateAccount.



A Frappe child table: rows are written through the parent (JournalEntryTemplate), so this

service only reads. There is no upstream controller logic to port.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.journal_entry_template_account_domain.models.journal_entry_template_account import JournalEntryTemplateAccount

from app.accounts.journal_entry_template_account_domain.repositories.journal_entry_template_account_repository import (

    JournalEntryTemplateAccountRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JournalEntryTemplateAccountService"]





class JournalEntryTemplateAccountService:

    def __init__(self, repository: Optional[JournalEntryTemplateAccountRepository] = None) -> None:

        self.repository = repository or JournalEntryTemplateAccountRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JournalEntryTemplateAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Journal Entry Template Account", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JournalEntryTemplateAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JournalEntryTemplateAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
