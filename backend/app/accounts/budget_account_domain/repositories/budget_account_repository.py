"""Data access for BudgetAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.budget_account_domain.models.budget_account import BudgetAccount

from app.core.pagination import normalise_paging



__all__ = ["BudgetAccountRepository"]





class BudgetAccountRepository:

    model = BudgetAccount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[BudgetAccount]:

        return db.scalar(

            select(BudgetAccount).where(

                BudgetAccount.business_id == business_id, BudgetAccount.id == row_id

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

    ) -> tuple[Sequence[BudgetAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [BudgetAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(BudgetAccount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(BudgetAccount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(BudgetAccount)

            .where(*conditions)

            .order_by(BudgetAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


