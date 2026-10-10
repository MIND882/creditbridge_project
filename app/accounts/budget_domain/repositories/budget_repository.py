"""Data access for Budget. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.budget_domain.models.budget import Budget

from app.core.pagination import normalise_paging



__all__ = ["BudgetRepository"]





class BudgetRepository:

    model = Budget



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(Budget.budget_distribution)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[Budget]:

        return db.scalar(

            select(Budget).where(

                Budget.business_id == business_id, Budget.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[Budget]:

        return db.scalar(

            select(Budget).where(

                Budget.business_id == business_id, Budget.name == name

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

    ) -> tuple[Sequence[Budget], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [Budget.business_id == business_id]

        if not include_cancelled:

            conditions.append(Budget.docstatus != 2)

        if search:

            conditions.append(Budget.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(Budget).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(Budget)

            .where(*conditions)

            .order_by(Budget.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: Budget) -> Budget:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: Budget) -> None:

        db.delete(row)

        db.flush()
