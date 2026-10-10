"""Business logic for BomUpdateBatch.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_update_batch_domain.models.bom_update_batch import BomUpdateBatch

from app.manufacturing.bom_update_batch_domain.repositories.bom_update_batch_repository import (

    BomUpdateBatchRepository,

)

from app.manufacturing.bom_update_batch_domain.schemas.bom_update_batch import (

    BomUpdateBatchCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomUpdateBatchService"]





class BomUpdateBatchService:

    def __init__(self, repository: Optional[BomUpdateBatchRepository] = None) -> None:

        self.repository = repository or BomUpdateBatchRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomUpdateBatch:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Update Batch", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomUpdateBatch]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomUpdateBatch].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
