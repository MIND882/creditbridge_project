"""Data access for ShippingRule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.shipping_rule_domain.models.shipping_rule import ShippingRule

from app.core.pagination import normalise_paging



__all__ = ["ShippingRuleRepository"]





class ShippingRuleRepository:

    model = ShippingRule



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(ShippingRule.conditions), selectinload(ShippingRule.countries)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ShippingRule]:

        return db.scalar(

            select(ShippingRule).where(

                ShippingRule.business_id == business_id, ShippingRule.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ShippingRule]:

        return db.scalar(

            select(ShippingRule).where(

                ShippingRule.business_id == business_id, ShippingRule.name == name

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

    ) -> tuple[Sequence[ShippingRule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ShippingRule.business_id == business_id]

        if search:

            conditions.append(ShippingRule.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ShippingRule).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ShippingRule)

            .where(*conditions)

            .order_by(ShippingRule.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: ShippingRule) -> ShippingRule:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ShippingRule) -> None:

        db.delete(row)

        db.flush()
