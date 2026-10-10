"""Business logic for TaxWithholdingEntry.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.tax_withholding_entry_domain.models.tax_withholding_entry import TaxWithholdingEntry

from app.accounts.tax_withholding_entry_domain.repositories.tax_withholding_entry_repository import (

    TaxWithholdingEntryRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["TaxWithholdingEntryService"]





class TaxWithholdingEntryService:

    def __init__(self, repository: Optional[TaxWithholdingEntryRepository] = None) -> None:

        self.repository = repository or TaxWithholdingEntryRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> TaxWithholdingEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Tax Withholding Entry", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[TaxWithholdingEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[TaxWithholdingEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
