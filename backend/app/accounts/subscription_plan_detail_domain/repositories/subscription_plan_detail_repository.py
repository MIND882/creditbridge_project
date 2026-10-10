"""Data access for SubscriptionPlanDetail. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.subscription_plan_detail_domain.models.subscription_plan_detail import SubscriptionPlanDetail

from app.core.pagination import normalise_paging



__all__ = ["SubscriptionPlanDetailRepository"]





class SubscriptionPlanDetailRepository:

    model = SubscriptionPlanDetail





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[SubscriptionPlanDetail]:

        return db.scalar(

            select(SubscriptionPlanDetail).where(

                SubscriptionPlanDetail.business_id == business_id, SubscriptionPlanDetail.id == row_id

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

    ) -> tuple[Sequence[SubscriptionPlanDetail], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [SubscriptionPlanDetail.business_id == business_id]

        if parent_id is not None:

            conditions.append(SubscriptionPlanDetail.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(SubscriptionPlanDetail).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(SubscriptionPlanDetail)

            .where(*conditions)

            .order_by(SubscriptionPlanDetail.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


