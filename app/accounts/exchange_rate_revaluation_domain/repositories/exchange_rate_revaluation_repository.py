"""Data access for ExchangeRateRevaluation. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.exchange_rate_revaluation_domain.models.exchange_rate_revaluation import ExchangeRateRevaluation

from app.core.pagination import normalise_paging



__all__ = ["ExchangeRateRevaluationRepository"]





class ExchangeRateRevaluationRepository:

    model = ExchangeRateRevaluation



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(ExchangeRateRevaluation.accounts)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[ExchangeRateRevaluation]:

        return db.scalar(

            select(ExchangeRateRevaluation).where(

                ExchangeRateRevaluation.business_id == business_id, ExchangeRateRevaluation.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[ExchangeRateRevaluation]:

        return db.scalar(

            select(ExchangeRateRevaluation).where(

                ExchangeRateRevaluation.business_id == business_id, ExchangeRateRevaluation.name == name

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

        include_cancelled: bool = False,

    ) -> tuple[Sequence[ExchangeRateRevaluation], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [ExchangeRateRevaluation.business_id == business_id]

        if not include_cancelled:

            conditions.append(ExchangeRateRevaluation.docstatus != 2)

        if search:

            conditions.append(ExchangeRateRevaluation.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(ExchangeRateRevaluation).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(ExchangeRateRevaluation)

            .where(*conditions)

            .order_by(ExchangeRateRevaluation.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: ExchangeRateRevaluation) -> ExchangeRateRevaluation:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: ExchangeRateRevaluation) -> None:

        db.delete(row)

        db.flush()
