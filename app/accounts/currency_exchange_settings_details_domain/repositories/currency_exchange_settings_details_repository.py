"""Data access for CurrencyExchangeSettingsDetails. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.accounts.currency_exchange_settings_details_domain.models.currency_exchange_settings_details import CurrencyExchangeSettingsDetails

from app.core.pagination import normalise_paging



__all__ = ["CurrencyExchangeSettingsDetailsRepository"]





class CurrencyExchangeSettingsDetailsRepository:

    model = CurrencyExchangeSettingsDetails





    def get_by_id(

        self, db: Session, business_id: uuid.UUID, row_id: uuid.UUID

    ) -> Optional[CurrencyExchangeSettingsDetails]:

        return db.scalar(

            select(CurrencyExchangeSettingsDetails).where(

                CurrencyExchangeSettingsDetails.business_id == business_id, CurrencyExchangeSettingsDetails.id == row_id

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

    ) -> tuple[Sequence[CurrencyExchangeSettingsDetails], int]:

        offset, limit = normalise_paging(offset, limit)

        conditions = [CurrencyExchangeSettingsDetails.business_id == business_id]

        if parent_id is not None:

            conditions.append(CurrencyExchangeSettingsDetails.parent_id == parent_id)



        total = int(

            db.scalar(select(func.count()).select_from(CurrencyExchangeSettingsDetails).where(*conditions))

            or 0

        )

        rows = db.scalars(

            select(CurrencyExchangeSettingsDetails)

            .where(*conditions)

            .order_by(CurrencyExchangeSettingsDetails.idx.asc())

            .offset(offset)

            .limit(limit)

        ).all()

        return rows, total


