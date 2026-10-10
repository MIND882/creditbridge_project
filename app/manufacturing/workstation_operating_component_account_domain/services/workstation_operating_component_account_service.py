"""Business logic for WorkstationOperatingComponentAccount.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.workstation_operating_component_account_domain.models.workstation_operating_component_account import WorkstationOperatingComponentAccount

from app.manufacturing.workstation_operating_component_account_domain.repositories.workstation_operating_component_account_repository import (

    WorkstationOperatingComponentAccountRepository,

)

from app.manufacturing.workstation_operating_component_account_domain.schemas.workstation_operating_component_account import (

    WorkstationOperatingComponentAccountCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["WorkstationOperatingComponentAccountService"]





class WorkstationOperatingComponentAccountService:

    def __init__(self, repository: Optional[WorkstationOperatingComponentAccountRepository] = None) -> None:

        self.repository = repository or WorkstationOperatingComponentAccountRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> WorkstationOperatingComponentAccount:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Workstation Operating Component Account", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[WorkstationOperatingComponentAccount]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[WorkstationOperatingComponentAccount].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
