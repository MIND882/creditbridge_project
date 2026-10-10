"""Business logic for SalesTeam.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.sales_team_domain.models.sales_team import SalesTeam

from app.selling.sales_team_domain.repositories.sales_team_repository import (

    SalesTeamRepository,

)

from app.selling.sales_team_domain.schemas.sales_team import (

    SalesTeamCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SalesTeamService"]





class SalesTeamService:

    def __init__(self, repository: Optional[SalesTeamRepository] = None) -> None:

        self.repository = repository or SalesTeamRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SalesTeam:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Sales Team", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SalesTeam]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SalesTeam].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
