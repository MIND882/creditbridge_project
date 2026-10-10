"""Data access for SubscriptionPlan. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_plan_domain.models.subscription_plan import SubscriptionPlan

from app.core.pagination import normalise_paging



__all__ = ["SubscriptionPlanRepository"]





class SubscriptionPlanRepository:

    model = SubscriptionPlan





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SubscriptionPlan]:

        return db.scalar(

            select(SubscriptionPlan).where(

                SubscriptionPlan.business_id == business_id, SubscriptionPlan.id == row_id

            )

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[SubscriptionPlan]:

        return db.scalar(

            select(SubscriptionPlan).where(

                SubscriptionPlan.business_id == business_id, SubscriptionPlan.name == name

            )

        )





    def list(

        self,

        db: Session,

        business_id: uuid.UUID,

        *,

        offset: int = 0,

        limit: int = 20,

        search: Optional[str] = None,

    ) -> tuple[Sequence[SubscriptionPlan], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SubscriptionPlan.business_id == business_id]

        if search:

            conditions.append(SubscriptionPlan.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(SubscriptionPlan).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SubscriptionPlan)

            .where(*conditions)

            .order_by(SubscriptionPlan.name.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total





    def add(self, db: Session, row: SubscriptionPlan) -> SubscriptionPlan:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: SubscriptionPlan) -> None:

        db.delete(row)

        db.flush()
