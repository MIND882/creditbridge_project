"""Business logic for SupplierScorecardScoringStanding.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.supplier_scorecard_scoring_standing_domain.models.supplier_scorecard_scoring_standing import SupplierScorecardScoringStanding

from app.buying.supplier_scorecard_scoring_standing_domain.repositories.supplier_scorecard_scoring_standing_repository import (

    SupplierScorecardScoringStandingRepository,

)

from app.buying.supplier_scorecard_scoring_standing_domain.schemas.supplier_scorecard_scoring_standing import (

    SupplierScorecardScoringStandingCreate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SupplierScorecardScoringStandingService"]





class SupplierScorecardScoringStandingService:

    def __init__(self, repository: Optional[SupplierScorecardScoringStandingRepository] = None) -> None:

        self.repository = repository or SupplierScorecardScoringStandingRepository()





    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SupplierScorecardScoringStanding:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Supplier Scorecard Scoring Standing", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SupplierScorecardScoringStanding]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SupplierScorecardScoringStanding].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
