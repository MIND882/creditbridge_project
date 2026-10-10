"""Business logic for SerialAndBatchEntry.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.serial_and_batch_entry_domain.models.serial_and_batch_entry import SerialAndBatchEntry

from app.stock.serial_and_batch_entry_domain.repositories.serial_and_batch_entry_repository import (

    SerialAndBatchEntryRepository,

)

from app.stock.serial_and_batch_entry_domain.schemas.serial_and_batch_entry import (

    SerialAndBatchEntryCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SerialAndBatchEntryService"]





class SerialAndBatchEntryService:

    def __init__(self, repository: Optional[SerialAndBatchEntryRepository] = None) -> None:

        self.repository = repository or SerialAndBatchEntryRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SerialAndBatchEntry:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Serial and Batch Entry", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SerialAndBatchEntry]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SerialAndBatchEntry].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
