"""Data access for DeliverySettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.delivery_settings_domain.models.delivery_settings import DeliverySettings

from app.core.pagination import normalise_paging



__all__ = ["DeliverySettingsRepository"]





class DeliverySettingsRepository:

    model = DeliverySettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[DeliverySettings]:

        return db.scalar(

            select(DeliverySettings).where(

                DeliverySettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: DeliverySettings) -> DeliverySettings:

        db.add(row)

        db.flush()

        return row
