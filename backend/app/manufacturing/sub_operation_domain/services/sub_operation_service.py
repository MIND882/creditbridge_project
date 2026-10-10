"""Business logic for SubOperation.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.sub_operation_domain.models.sub_operation import SubOperation

from app.manufacturing.sub_operation_domain.repositories.sub_operation_repository import (

    SubOperationRepository,

)

from app.manufacturing.sub_operation_domain.schemas.sub_operation import (

    SubOperationCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubOperationService"]





class SubOperationService:

    def __init__(self, repository: Optional[SubOperationRepository] = None) -> None:

        self.repository = repository or SubOperationRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubOperation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sub Operation", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SubOperation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SubOperation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
