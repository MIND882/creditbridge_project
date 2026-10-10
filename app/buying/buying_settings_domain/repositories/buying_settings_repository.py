"""Data access for BuyingSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.buying.buying_settings_domain.models.buying_settings import BuyingSettings

from app.core.pagination import normalise_paging



__all__ = ["BuyingSettingsRepository"]





class BuyingSettingsRepository:

    model = BuyingSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[BuyingSettings]:

        return db.scalar(

            select(BuyingSettings).where(

                BuyingSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: BuyingSettings) -> BuyingSettings:

        db.add(row)

        db.flush()

        return row
