"""

Business logic for Cost Center Allocation Percentage.



Rows are owned by a Cost Center Allocation, so the write path lives in

``CostCenterAllocationService`` (which enforces the 100% total and the

main/child exclusivity rules). This service covers the read side plus the one

rule that belongs to the row itself: ``percentage`` must be a positive Percent.

"""



from __future__ import annotations



import uuid

from decimal import Decimal

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.cost_center_allocation_percentage_domain.repositories.cost_center_allocation_percentage_repository import (

    CostCenterAllocationPercentageRepository,

)

from app.core.errors import DomainValidationError, NotFoundError

from app.core.pagination import ResultPage



__all__ = ["CostCenterAllocationPercentageService"]





class CostCenterAllocationPercentageService:

    def __init__(

        self,

        repository: Optional[CostCenterAllocationPercentageRepository] = None,

    ) -> None:

        self.repository = repository or CostCenterAllocationPercentageRepository()



    @staticmethod

    def validate_percentage(percentage: Decimal) -> None:

        """

        ERPNext `Percent` is 0..100; a split row must be strictly positive

        because a 0% row would be a silent no-op.

        """

        if percentage is None or percentage <= 0:

            raise DomainValidationError(

                "Percentage must be greater than 0", code="allocation_percentage_not_positive"

            )

        if percentage > Decimal("100"):

            raise DomainValidationError(

                "Percentage cannot exceed 100", code="allocation_percentage_over_100"

            )



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ):

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Cost Center Allocation Percentage", row_id)

        return row



    def list_by_parent(

        self, db: Session, business_id: uuid.UUID, parent_id: uuid.UUID

    ) -> list:

        return self.repository.list_by_parent(db, business_id, parent_id)



    def list(self, db: Session, business_id: uuid.UUID, **filters: object):

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage.build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
