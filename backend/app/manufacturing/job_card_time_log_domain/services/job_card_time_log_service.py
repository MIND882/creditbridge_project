"""Business logic for JobCardTimeLog.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.job_card_time_log_domain.models.job_card_time_log import JobCardTimeLog

from app.manufacturing.job_card_time_log_domain.repositories.job_card_time_log_repository import (

    JobCardTimeLogRepository,

)

from app.manufacturing.job_card_time_log_domain.schemas.job_card_time_log import (

    JobCardTimeLogCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JobCardTimeLogService"]





class JobCardTimeLogService:

    def __init__(self, repository: Optional[JobCardTimeLogRepository] = None) -> None:

        self.repository = repository or JobCardTimeLogRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCardTimeLog:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Job Card Time Log", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JobCardTimeLog]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JobCardTimeLog].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
