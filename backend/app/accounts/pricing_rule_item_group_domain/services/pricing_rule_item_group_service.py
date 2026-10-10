"""Business logic for PricingRuleItemGroup.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.pricing_rule_item_group_domain.models.pricing_rule_item_group import PricingRuleItemGroup

from app.accounts.pricing_rule_item_group_domain.repositories.pricing_rule_item_group_repository import (

    PricingRuleItemGroupRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["PricingRuleItemGroupService"]





class PricingRuleItemGroupService:

    def __init__(self, repository: Optional[PricingRuleItemGroupRepository] = None) -> None:

        self.repository = repository or PricingRuleItemGroupRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> PricingRuleItemGroup:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Pricing Rule Item Group", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[PricingRuleItemGroup]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[PricingRuleItemGroup].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
