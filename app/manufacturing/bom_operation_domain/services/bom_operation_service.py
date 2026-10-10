"""Business logic for BomOperation.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.bom_operation_domain.models.bom_operation import BomOperation

from app.manufacturing.bom_operation_domain.repositories.bom_operation_repository import (

    BomOperationRepository,

)

from app.manufacturing.bom_operation_domain.schemas.bom_operation import (

    BomOperationCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BomOperationService"]





class BomOperationService:

    def __init__(self, repository: Optional[BomOperationRepository] = None) -> None:

        self.repository = repository or BomOperationRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BomOperation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("BOM Operation", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BomOperation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BomOperation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
