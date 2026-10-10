"""Business logic for ShippingRuleCondition.



A Frappe child table: rows are written through the parent, so this service only

reads. Upstream declares no controller logic for it.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.accounts.shipping_rule_condition_domain.models.shipping_rule_condition import ShippingRuleCondition

from app.accounts.shipping_rule_condition_domain.repositories.shipping_rule_condition_repository import (

    ShippingRuleConditionRepository,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ShippingRuleConditionService"]





class ShippingRuleConditionService:

    def __init__(self, repository: Optional[ShippingRuleConditionRepository] = None) -> None:

        self.repository = repository or ShippingRuleConditionRepository()



    def get(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> ShippingRuleCondition:

        row = self.repository.get_by_id(db, business_id, row_id)

        if row is None:

            raise NotFoundError("Shipping Rule Condition", row_id)

        return row



    def list(

        self, db: Session, business_id: uuid.UUID, **filters: object

    ) -> ResultPage[ShippingRuleCondition]:

        rows, total = self.repository.list(db, business_id, **filters)  # type: ignore[arg-type]

        return ResultPage[ShippingRuleCondition].build(

            rows,

            total=total,

            offset=int(filters.get("offset", 0)),  # type: ignore[arg-type]

            limit=int(filters.get("limit", 20)),  # type: ignore[arg-type]

        )
