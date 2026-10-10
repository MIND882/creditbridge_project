"""Data access for StockSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.stock_settings_domain.models.stock_settings import StockSettings

from app.core.pagination import normalise_paging



__all__ = ["StockSettingsRepository"]





class StockSettingsRepository:

    model = StockSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[StockSettings]:

        return db.scalar(

            select(StockSettings).where(

                StockSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: StockSettings) -> StockSettings:

        db.add(row)

        db.flush()

        return row
