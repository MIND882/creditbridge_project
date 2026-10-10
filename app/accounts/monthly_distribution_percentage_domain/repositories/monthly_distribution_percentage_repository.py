"""Data access for MonthlyDistributionPercentage. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.monthly_distribution_percentage_domain.models.monthly_distribution_percentage import MonthlyDistributionPercentage

from app.core.pagination import normalise_paging



__all__ = ["MonthlyDistributionPercentageRepository"]





class MonthlyDistributionPercentageRepository:

    model = MonthlyDistributionPercentage





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MonthlyDistributionPercentage]:

        return db.scalar(

            select(MonthlyDistributionPercentage).where(

                MonthlyDistributionPercentage.business_id == business_id, MonthlyDistributionPercentage.id == row_id

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

    ) -> tuple[Sequence[MonthlyDistributionPercentage], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MonthlyDistributionPercentage.business_id == business_id]

        if parent_id is not None:

            conditions.append(MonthlyDistributionPercentage.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(MonthlyDistributionPercentage).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MonthlyDistributionPercentage)

            .where(*conditions)

            .order_by(MonthlyDistributionPercentage.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


