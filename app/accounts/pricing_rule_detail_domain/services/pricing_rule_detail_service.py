"""Business logic for PricingRuleDetail.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.accounts.pricing_rule_detail_domain.repositories.pricing_rule_detail_repository import (

    PricingRuleDetailRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PricingRuleDetailService"]





class PricingRuleDetailService:

    def __init__(self, repository: Optional[PricingRuleDetailRepository] = None) -> None:

        self.repository = repository or PricingRuleDetailRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PricingRuleDetail:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pricing Rule Detail", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PricingRuleDetail]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PricingRuleDetail].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
