"""Business logic for WorkOrderOperation.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.work_order_operation_domain.models.work_order_operation import WorkOrderOperation

from app.manufacturing.work_order_operation_domain.repositories.work_order_operation_repository import (

    WorkOrderOperationRepository,

)

from app.manufacturing.work_order_operation_domain.schemas.work_order_operation import (

    WorkOrderOperationCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkOrderOperationService"]





class WorkOrderOperationService:

    def __init__(self, repository: Optional[WorkOrderOperationRepository] = None) -> None:

        self.repository = repository or WorkOrderOperationRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkOrderOperation:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Work Order Operation", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkOrderOperation]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkOrderOperation].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
