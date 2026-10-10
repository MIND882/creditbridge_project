"""Data access for PromotionalScheme. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.promotional_scheme_domain.models.promotional_scheme import PromotionalScheme

from app.core.pagination import normalise_paging



__all__ = ["PromotionalSchemeRepository"]





class PromotionalSchemeRepository:

    model = PromotionalScheme



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PromotionalScheme.items), selectinload(PromotionalScheme.item_groups), selectinload(PromotionalScheme.brands), selectinload(PromotionalScheme.customer), selectinload(PromotionalScheme.customer_group), selectinload(PromotionalScheme.territory), selectinload(PromotionalScheme.sales_partner), selectinload(PromotionalScheme.campaign), selectinload(PromotionalScheme.supplier), selectinload(PromotionalScheme.supplier_group), selectinload(PromotionalScheme.price_discount_slabs), selectinload(PromotionalScheme.product_discount_slabs)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PromotionalScheme]:

        return db.scalar(

            select(PromotionalScheme).where(

                PromotionalScheme.business_id == business_id, PromotionalScheme.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PromotionalScheme]:

        return db.scalar(

            select(PromotionalScheme).where(

                PromotionalScheme.business_id == business_id, PromotionalScheme.name == name

            ).options(*self._options())

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[PromotionalScheme], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PromotionalScheme.business_id == business_id]

        if search:

            conditions.append(PromotionalScheme.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PromotionalScheme).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PromotionalScheme)

            .where(*conditions)

            .order_by(PromotionalScheme.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PromotionalScheme) -> PromotionalScheme:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PromotionalScheme) -> None:

        db.delete(row)

        db.flush()
