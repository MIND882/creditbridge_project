"""Data access for StockRepostingSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_reposting_settings_domain.models.stock_reposting_settings import StockRepostingSettings

from app.core.pagination import normalise_paging



__all__ = ["StockRepostingSettingsRepository"]





class StockRepostingSettingsRepository:

    model = StockRepostingSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[StockRepostingSettings]:

        return db.scalar(

            select(StockRepostingSettings).where(

                StockRepostingSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: StockRepostingSettings) -> StockRepostingSettings:

        db.add(row)

        db.flush()

        return row
