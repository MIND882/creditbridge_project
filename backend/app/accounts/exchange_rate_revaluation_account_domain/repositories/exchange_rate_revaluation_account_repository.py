"""Data access for ExchangeRateRevaluationAccount. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.exchange_rate_revaluation_account_domain.models.exchange_rate_revaluation_account import ExchangeRateRevaluationAccount

from app.core.pagination import normalise_paging



__all__ = ["ExchangeRateRevaluationAccountRepository"]





class ExchangeRateRevaluationAccountRepository:

    model = ExchangeRateRevaluationAccount





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ExchangeRateRevaluationAccount]:

        return db.scalar(

            select(ExchangeRateRevaluationAccount).where(

                ExchangeRateRevaluationAccount.business_id == business_id, ExchangeRateRevaluationAccount.id == row_id

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

    ) -> tuple[Sequence[ExchangeRateRevaluationAccount], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ExchangeRateRevaluationAccount.business_id == business_id]

        if parent_id is not None:

            conditions.append(ExchangeRateRevaluationAccount.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(ExchangeRateRevaluationAccount).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ExchangeRateRevaluationAccount)

            .where(*conditions)

            .order_by(ExchangeRateRevaluationAccount.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


