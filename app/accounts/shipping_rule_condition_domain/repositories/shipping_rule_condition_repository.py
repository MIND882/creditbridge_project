"""Data access for ShippingRuleCondition. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.shipping_rule_condition_domain.models.shipping_rule_condition import ShippingRuleCondition

from app.core.pagination import normalise_paging



__all__ = ["ShippingRuleConditionRepository"]





class ShippingRuleConditionRepository:

    model = ShippingRuleCondition





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShippingRuleCondition]:

        return db.scalar(

            select(ShippingRuleCondition).where(

                ShippingRuleCondition.business_id == business_id, ShippingRuleCondition.id == row_id

            )

        )







    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20, 

        parent_id: Optional[uuid.UUID] = None,

    ) -> tuple[Sequence[ShippingRuleCondition], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShippingRuleCondition.business_id == business_id]

        if parent_id is not None:

            conditions.append(ShippingRuleCondition.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ShippingRuleCondition).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShippingRuleCondition)

            .where(*conditions)

            .order_by(ShippingRuleCondition.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


