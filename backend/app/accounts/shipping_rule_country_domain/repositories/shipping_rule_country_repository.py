"""Data access for ShippingRuleCountry. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.shipping_rule_country_domain.models.shipping_rule_country import ShippingRuleCountry

from app.core.pagination import normalise_paging



__all__ = ["ShippingRuleCountryRepository"]





class ShippingRuleCountryRepository:

    model = ShippingRuleCountry





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShippingRuleCountry]:

        return db.scalar(

            select(ShippingRuleCountry).where(

                ShippingRuleCountry.business_id == business_id, ShippingRuleCountry.id == row_id

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

    ) -> tuple[Sequence[ShippingRuleCountry], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShippingRuleCountry.business_id == business_id]

        if parent_id is not None:

            conditions.append(ShippingRuleCountry.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ShippingRuleCountry).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShippingRuleCountry)

            .where(*conditions)

            .order_by(ShippingRuleCountry.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


