"""Business logic for JobCardOperation.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.job_card_operation_domain.models.job_card_operation import JobCardOperation

from app.manufacturing.job_card_operation_domain.repositories.job_card_operation_repository import (

    JobCardOperationRepository,

)

from app.manufacturing.job_card_operation_domain.schemas.job_card_operation import (

    JobCardOperationCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JobCardOperationService"]





class JobCardOperationService:

    def __init__(self, repository: Optional[JobCardOperationRepository] = None) -> None:

        self.repository = repository or JobCardOperationRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCardOperation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Job Card Operation", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JobCardOperation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JobCardOperation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
