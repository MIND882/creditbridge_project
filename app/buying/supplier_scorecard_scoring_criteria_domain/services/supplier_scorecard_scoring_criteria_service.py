"""Business logic for SupplierScorecardScoringCriteria.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_criteria_domain.models.supplier_scorecard_scoring_criteria import SupplierScorecardScoringCriteria

from app.buying.supplier_scorecard_scoring_criteria_domain.repositories.supplier_scorecard_scoring_criteria_repository import (

    SupplierScorecardScoringCriteriaRepository,

)

from app.buying.supplier_scorecard_scoring_criteria_domain.schemas.supplier_scorecard_scoring_criteria import (

    SupplierScorecardScoringCriteriaCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardScoringCriteriaService"]





class SupplierScorecardScoringCriteriaService:

    def __init__(self, repository: Optional[SupplierScorecardScoringCriteriaRepository] = None) -> None:

        self.repository = repository or SupplierScorecardScoringCriteriaRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardScoringCriteria:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Scoring Criteria", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardScoringCriteria]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardScoringCriteria].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
