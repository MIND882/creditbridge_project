"""Data access for PricingRule. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pricing_rule_domain.models.pricing_rule import PricingRule

from app.core.pagination import normalise_paging



__all__ = ["PricingRuleRepository"]





class PricingRuleRepository:

    model = PricingRule



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PricingRule.items), selectinload(PricingRule.item_groups), selectinload(PricingRule.brands)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PricingRule]:

        return db.scalar(

            select(PricingRule).where(

                PricingRule.business_id == business_id, PricingRule.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PricingRule]:

        return db.scalar(

            select(PricingRule).where(

                PricingRule.business_id == business_id, PricingRule.name == name

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

    ) -> tuple[Sequence[PricingRule], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PricingRule.business_id == business_id]

        if search:

            conditions.append(PricingRule.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PricingRule).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PricingRule)

            .where(*conditions)

            .order_by(PricingRule.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PricingRule) -> PricingRule:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PricingRule) -> None:

        db.delete(row)

        db.flush()
