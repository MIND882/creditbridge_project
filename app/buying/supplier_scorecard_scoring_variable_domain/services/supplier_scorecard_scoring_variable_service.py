"""Business logic for SupplierScorecardScoringVariable.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_variable_domain.models.supplier_scorecard_scoring_variable import SupplierScorecardScoringVariable

from app.buying.supplier_scorecard_scoring_variable_domain.repositories.supplier_scorecard_scoring_variable_repository import (

    SupplierScorecardScoringVariableRepository,

)

from app.buying.supplier_scorecard_scoring_variable_domain.schemas.supplier_scorecard_scoring_variable import (

    SupplierScorecardScoringVariableCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardScoringVariableService"]





class SupplierScorecardScoringVariableService:

    def __init__(self, repository: Optional[SupplierScorecardScoringVariableRepository] = None) -> None:

        self.repository = repository or SupplierScorecardScoringVariableRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardScoringVariable:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Scoring Variable", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardScoringVariable]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardScoringVariable].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
