"""Data access for Subscription. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.subscription_domain.models.subscription import Subscription

from app.core.pagination import normalise_paging



__all__ = ["SubscriptionRepository"]





class SubscriptionRepository:

    model = Subscription



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(Subscription.plans)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Subscription]:

        return db.scalar(

            select(Subscription).where(

                Subscription.business_id == business_id, Subscription.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Subscription]:

        return db.scalar(

            select(Subscription).where(

                Subscription.business_id == business_id, Subscription.name == name

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

    ) -> tuple[Sequence[Subscription], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Subscription.business_id == business_id]

        if search:

            conditions.append(Subscription.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Subscription).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Subscription)

            .where(*conditions)

            .order_by(Subscription.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: Subscription) -> Subscription:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Subscription) -> None:

        db.delete(row)

        db.flush()
