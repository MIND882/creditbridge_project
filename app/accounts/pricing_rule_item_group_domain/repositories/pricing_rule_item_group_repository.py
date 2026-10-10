"""Data access for PricingRuleItemGroup. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_item_group_domain.models.pricing_rule_item_group import PricingRuleItemGroup

from app.core.pagination import normalise_paging



__all__ = ["PricingRuleItemGroupRepository"]





class PricingRuleItemGroupRepository:

    model = PricingRuleItemGroup





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PricingRuleItemGroup]:

        return db.scalar(

            select(PricingRuleItemGroup).where(

                PricingRuleItemGroup.business_id == business_id, PricingRuleItemGroup.id == row_id

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

    ) -> tuple[Sequence[PricingRuleItemGroup], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PricingRuleItemGroup.business_id == business_id]

        if parent_id is not None:

            conditions.append(PricingRuleItemGroup.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PricingRuleItemGroup).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PricingRuleItemGroup)

            .where(*conditions)

            .order_by(PricingRuleItemGroup.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


