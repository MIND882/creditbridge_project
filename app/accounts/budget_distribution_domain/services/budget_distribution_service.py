"""Business logic for BudgetDistribution.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.budget_distribution_domain.models.budget_distribution import BudgetDistribution

from app.accounts.budget_distribution_domain.repositories.budget_distribution_repository import (

    BudgetDistributionRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BudgetDistributionService"]





class BudgetDistributionService:

    def __init__(self, repository: Optional[BudgetDistributionRepository] = None) -> None:

        self.repository = repository or BudgetDistributionRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> BudgetDistribution:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Budget Distribution", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[BudgetDistribution]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[BudgetDistribution].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
