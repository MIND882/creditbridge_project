"""Business logic for JobCardScheduledTime.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.job_card_scheduled_time_domain.models.job_card_scheduled_time import JobCardScheduledTime

from app.manufacturing.job_card_scheduled_time_domain.repositories.job_card_scheduled_time_repository import (

    JobCardScheduledTimeRepository,

)

from app.manufacturing.job_card_scheduled_time_domain.schemas.job_card_scheduled_time import (

    JobCardScheduledTimeCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JobCardScheduledTimeService"]





class JobCardScheduledTimeService:

    def __init__(self, repository: Optional[JobCardScheduledTimeRepository] = None) -> None:

        self.repository = repository or JobCardScheduledTimeRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCardScheduledTime:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Job Card Scheduled Time", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JobCardScheduledTime]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JobCardScheduledTime].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
