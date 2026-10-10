"""Data access for CurrencyExchangeSettingsResult. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.currency_exchange_settings_result_domain.models.currency_exchange_settings_result import CurrencyExchangeSettingsResult

from app.core.pagination import normalise_paging



__all__ = ["CurrencyExchangeSettingsResultRepository"]





class CurrencyExchangeSettingsResultRepository:

    model = CurrencyExchangeSettingsResult





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CurrencyExchangeSettingsResult]:

        return db.scalar(

            select(CurrencyExchangeSettingsResult).where(

                CurrencyExchangeSettingsResult.business_id == business_id, CurrencyExchangeSettingsResult.id == row_id

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

    ) -> tuple[Sequence[CurrencyExchangeSettingsResult], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CurrencyExchangeSettingsResult.business_id == business_id]

        if parent_id is not None:

            conditions.append(CurrencyExchangeSettingsResult.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CurrencyExchangeSettingsResult).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CurrencyExchangeSettingsResult)

            .where(*conditions)

            .order_by(CurrencyExchangeSettingsResult.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


