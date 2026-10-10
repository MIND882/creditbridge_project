"""Data access for PeggedCurrencies. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.pegged_currencies_domain.models.pegged_currencies import PeggedCurrencies

from app.core.pagination import normalise_paging



__all__ = ["PeggedCurrenciesRepository"]





class PeggedCurrenciesRepository:

    model = PeggedCurrencies



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(PeggedCurrencies.pegged_currency_item)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[PeggedCurrencies]:

        return db.scalar(

            select(PeggedCurrencies).where(

                PeggedCurrencies.business_id == business_id, PeggedCurrencies.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[PeggedCurrencies]:

        return db.scalar(

            select(PeggedCurrencies).where(

                PeggedCurrencies.business_id == business_id, PeggedCurrencies.name == name

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

    ) -> tuple[Sequence[PeggedCurrencies], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [PeggedCurrencies.business_id == business_id]

        if search:

            conditions.append(PeggedCurrencies.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(PeggedCurrencies).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(PeggedCurrencies)

            .where(*conditions)

            .order_by(PeggedCurrencies.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: PeggedCurrencies) -> PeggedCurrencies:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: PeggedCurrencies) -> None:

        db.delete(row)

        db.flush()
