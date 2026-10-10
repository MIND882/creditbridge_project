"""Data access for PricingRuleBrand. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.pricing_rule_brand_domain.models.pricing_rule_brand import PricingRuleBrand

from app.core.pagination import normalise_paging



__all__ = ["PricingRuleBrandRepository"]





class PricingRuleBrandRepository:

    model = PricingRuleBrand





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PricingRuleBrand]:

        return db.scalar(

            select(PricingRuleBrand).where(

                PricingRuleBrand.business_id == business_id, PricingRuleBrand.id == row_id

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

    ) -> tuple[Sequence[PricingRuleBrand], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PricingRuleBrand.business_id == business_id]

        if parent_id is not None:

            conditions.append(PricingRuleBrand.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PricingRuleBrand).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PricingRuleBrand)

            .where(*conditions)

            .order_by(PricingRuleBrand.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


