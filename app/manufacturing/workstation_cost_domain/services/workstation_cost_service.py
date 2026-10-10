"""Business logic for WorkstationCost.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.workstation_cost_domain.models.workstation_cost import WorkstationCost

from app.manufacturing.workstation_cost_domain.repositories.workstation_cost_repository import (

    WorkstationCostRepository,

)

from app.manufacturing.workstation_cost_domain.schemas.workstation_cost import (

    WorkstationCostCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkstationCostService"]





class WorkstationCostService:

    def __init__(self, repository: Optional[WorkstationCostRepository] = None) -> None:

        self.repository = repository or WorkstationCostRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationCost:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Workstation Cost", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkstationCost]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkstationCost].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
