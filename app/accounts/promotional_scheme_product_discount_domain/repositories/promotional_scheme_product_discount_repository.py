"""Data access for PromotionalSchemeProductDiscount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.promotional_scheme_product_discount_domain.models.promotional_scheme_product_discount import PromotionalSchemeProductDiscount

from app.core.pagination import normalise_paging



__all__ = ["PromotionalSchemeProductDiscountRepository"]





class PromotionalSchemeProductDiscountRepository:

    model = PromotionalSchemeProductDiscount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PromotionalSchemeProductDiscount]:

        return db.scalar(

            select(PromotionalSchemeProductDiscount).where(

                PromotionalSchemeProductDiscount.business_id == business_id, PromotionalSchemeProductDiscount.id == row_id

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

    ) -> tuple[Sequence[PromotionalSchemeProductDiscount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PromotionalSchemeProductDiscount.business_id == business_id]

        if parent_id is not None:

            conditions.append(PromotionalSchemeProductDiscount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(PromotionalSchemeProductDiscount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PromotionalSchemeProductDiscount)

            .where(*conditions)

            .order_by(PromotionalSchemeProductDiscount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


