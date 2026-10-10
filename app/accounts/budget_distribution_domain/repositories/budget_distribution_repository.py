"""Data access for BudgetDistribution. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.budget_distribution_domain.models.budget_distribution import BudgetDistribution

from app.core.pagination import normalise_paging



__all__ = ["BudgetDistributionRepository"]





class BudgetDistributionRepository:

    model = BudgetDistribution





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BudgetDistribution]:

        return db.scalar(

            select(BudgetDistribution).where(

                BudgetDistribution.business_id == business_id, BudgetDistribution.id == row_id

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

    ) -> tuple[Sequence[BudgetDistribution], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BudgetDistribution.business_id == business_id]

        if parent_id is not None:

            conditions.append(BudgetDistribution.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BudgetDistribution).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BudgetDistribution)

            .where(*conditions)

            .order_by(BudgetDistribution.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


