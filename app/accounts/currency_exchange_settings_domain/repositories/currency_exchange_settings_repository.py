"""Data access for CurrencyExchangeSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session, selectinload



from app.accounts.currency_exchange_settings_domain.models.currency_exchange_settings import CurrencyExchangeSettings

from app.core.pagination import normalise_paging



__all__ = ["CurrencyExchangeSettingsRepository"]





class CurrencyExchangeSettingsRepository:

    model = CurrencyExchangeSettings



    @staticmethod

    def _options():

        # Built in a method, never as a class attribute: a class-level

        # selectinload() is evaluated at import time and breaks

        # conftest collection.

        return [selectinload(CurrencyExchangeSettings.req_params), selectinload(CurrencyExchangeSettings.result_key)]





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CurrencyExchangeSettings]:

        return db.scalar(

            select(CurrencyExchangeSettings).where(

                CurrencyExchangeSettings.business_id == business_id, CurrencyExchangeSettings.id == row_id

            ).options(*self._options())

        )





    def get_by_name(

        self, db: Session, business_id: uuid.UUID, name: str

    ) -> Optional[CurrencyExchangeSettings]:

        return db.scalar(

            select(CurrencyExchangeSettings).where(

                CurrencyExchangeSettings.business_id == business_id, CurrencyExchangeSettings.name == name

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

    ) -> tuple[Sequence[CurrencyExchangeSettings], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CurrencyExchangeSettings.business_id == business_id]

        if search:

            conditions.append(CurrencyExchangeSettings.name.ilike(f"%{search.strip()}%"))



        total = int(

            db.scalar(select(func.count()).select_from(CurrencyExchangeSettings).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CurrencyExchangeSettings)

            .where(*conditions)

            .order_by(CurrencyExchangeSettings.name.asc())

            .offset(offset)

            .limit(limit).options(*self._options())

        ).all()

        return rows, total





    def add(self, db: Session, row: CurrencyExchangeSettings) -> CurrencyExchangeSettings:

        db.add(row)

        db.flush()

        return row



    def delete(self, db: Session, row: CurrencyExchangeSettings) -> None:

        db.delete(row)

        db.flush()
