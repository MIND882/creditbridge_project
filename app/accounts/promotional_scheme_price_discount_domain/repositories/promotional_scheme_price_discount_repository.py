"""Data access for PromotionalSchemePriceDiscount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_price_discount_domain.models.promotional_scheme_price_discount import PromotionalSchemePriceDiscount

from app.core.pagination import normalise_paging



__all__ = ["PromotionalSchemePriceDiscountRepository"]





class PromotionalSchemePriceDiscountRepository:

    model = PromotionalSchemePriceDiscount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PromotionalSchemePriceDiscount]:

        return db.scalar(

            select(PromotionalSchemePriceDiscount).where(

                PromotionalSchemePriceDiscount.business_id == business_id, PromotionalSchemePriceDiscount.id == row_id

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

    ) -> tuple[Sequence[PromotionalSchemePriceDiscount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PromotionalSchemePriceDiscount.business_id == business_id]

        if parent_id is not None:

            conditions.append(PromotionalSchemePriceDiscount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PromotionalSchemePriceDiscount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PromotionalSchemePriceDiscount)

            .where(*conditions)

            .order_by(PromotionalSchemePriceDiscount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


