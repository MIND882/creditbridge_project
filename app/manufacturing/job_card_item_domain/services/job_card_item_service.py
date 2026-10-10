"""Business logic for JobCardItem.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.job_card_item_domain.models.job_card_item import JobCardItem

from app.manufacturing.job_card_item_domain.repositories.job_card_item_repository import (

    JobCardItemRepository,

)

from app.manufacturing.job_card_item_domain.schemas.job_card_item import (

    JobCardItemCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["JobCardItemService"]





class JobCardItemService:

    def __init__(self, repository: Optional[JobCardItemRepository] = None) -> None:

        self.repository = repository or JobCardItemRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> JobCardItem:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Job Card Item", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[JobCardItem]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[JobCardItem].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
