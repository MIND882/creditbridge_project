"""Business logic for PsoaCostCenter.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.psoa_cost_center_domain.models.psoa_cost_center import PsoaCostCenter

from app.accounts.psoa_cost_center_domain.repositories.psoa_cost_center_repository import (

    PsoaCostCenterRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PsoaCostCenterService"]





class PsoaCostCenterService:

    def __init__(self, repository: Optional[PsoaCostCenterRepository] = None) -> None:

        self.repository = repository or PsoaCostCenterRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PsoaCostCenter:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Psoa Cost Center", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PsoaCostCenter]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PsoaCostCenter].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
