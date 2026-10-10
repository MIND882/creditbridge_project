"""Data access for MonthlyDistribution. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.monthly_distribution_domain.models.monthly_distribution import MonthlyDistribution

from app.core.pagination import normalise_paging



__all__ = ["MonthlyDistributionRepository"]





class MonthlyDistributionRepository:

    model = MonthlyDistribution



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(MonthlyDistribution.percentages)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[MonthlyDistribution]:

        return db.scalar(

            select(MonthlyDistribution).where(

                MonthlyDistribution.business_id == business_id, MonthlyDistribution.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[MonthlyDistribution]:

        return db.scalar(

            select(MonthlyDistribution).where(

                MonthlyDistribution.business_id == business_id, MonthlyDistribution.name == name

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

    ) -> tuple[Sequence[MonthlyDistribution], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [MonthlyDistribution.business_id == business_id]

        if search:

            conditions.append(MonthlyDistribution.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(MonthlyDistribution).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(MonthlyDistribution)

            .where(*conditions)

            .order_by(MonthlyDistribution.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: MonthlyDistribution) -> MonthlyDistribution:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: MonthlyDistribution) -> None:

        db.delete(row)

        db.flush()
