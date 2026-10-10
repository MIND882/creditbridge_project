"""Business logic for MonthlyDistributionPercentage.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.monthly_distribution_percentage_domain.models.monthly_distribution_percentage import MonthlyDistributionPercentage

from app.accounts.monthly_distribution_percentage_domain.repositories.monthly_distribution_percentage_repository import (

    MonthlyDistributionPercentageRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["MonthlyDistributionPercentageService"]





class MonthlyDistributionPercentageService:

    def __init__(self, repository: Optional[MonthlyDistributionPercentageRepository] = None) -> None:

        self.repository = repository or MonthlyDistributionPercentageRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> MonthlyDistributionPercentage:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Monthly Distribution Percentage", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[MonthlyDistributionPercentage]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[MonthlyDistributionPercentage].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
