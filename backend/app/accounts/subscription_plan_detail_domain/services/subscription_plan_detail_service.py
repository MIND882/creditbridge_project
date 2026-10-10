"""Business logic for SubscriptionPlanDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail

from app.accounts.subscription_plan_detail_domain.repositories.subscription_plan_detail_repository import (

    SubscriptionPlanDetailRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SubscriptionPlanDetailService"]





class SubscriptionPlanDetailService:

    def __init__(self, repository: Optional[SubscriptionPlanDetailRepository] = None) -> None:

        self.repository = repository or SubscriptionPlanDetailRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> SubscriptionPlanDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Subscription Plan Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[SubscriptionPlanDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[SubscriptionPlanDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
