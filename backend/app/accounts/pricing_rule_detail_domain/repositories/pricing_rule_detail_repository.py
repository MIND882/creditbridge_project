"""Data access for PricingRuleDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_detail_domain.models.pricing_rule_detail import PricingRuleDetail

from app.core.pagination import normalise_paging



__all__ = ["PricingRuleDetailRepository"]





class PricingRuleDetailRepository:

    model = PricingRuleDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PricingRuleDetail]:

        return db.scalar(

            select(PricingRuleDetail).where(

                PricingRuleDetail.business_id == business_id, PricingRuleDetail.id == row_id

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

    ) -> tuple[Sequence[PricingRuleDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PricingRuleDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(PricingRuleDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PricingRuleDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PricingRuleDetail)

            .where(*conditions)

            .order_by(PricingRuleDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


