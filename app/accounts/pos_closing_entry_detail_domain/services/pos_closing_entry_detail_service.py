"""Business logic for POSClosingEntryDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pos_closing_entry_detail_domain.models.pos_closing_entry_detail import POSClosingEntryDetail

from app.accounts.pos_closing_entry_detail_domain.repositories.pos_closing_entry_detail_repository import (

    POSClosingEntryDetailRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["POSClosingEntryDetailService"]





class POSClosingEntryDetailService:

    def __init__(self, repository: Optional[POSClosingEntryDetailRepository] = None) -> None:

        self.repository = repository or POSClosingEntryDetailRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> POSClosingEntryDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("POS Closing Entry Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[POSClosingEntryDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[POSClosingEntryDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
