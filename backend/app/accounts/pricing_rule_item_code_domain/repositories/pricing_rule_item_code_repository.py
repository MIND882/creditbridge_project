"""Data access for PricingRuleItemCode. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_item_code_domain.models.pricing_rule_item_code import PricingRuleItemCode

from app.core.pagination import normalise_paging



__all__ = ["PricingRuleItemCodeRepository"]





class PricingRuleItemCodeRepository:

    model = PricingRuleItemCode





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PricingRuleItemCode]:

        return db.scalar(

            select(PricingRuleItemCode).where(

                PricingRuleItemCode.business_id == business_id, PricingRuleItemCode.id == row_id

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

    ) -> tuple[Sequence[PricingRuleItemCode], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PricingRuleItemCode.business_id == business_id]

        if parent_id is not None:

            conditions.append(PricingRuleItemCode.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PricingRuleItemCode).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PricingRuleItemCode)

            .where(*conditions)

            .order_by(PricingRuleItemCode.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


