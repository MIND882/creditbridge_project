"""Data access for SellingSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.selling.selling_settings_domain.models.selling_settings import SellingSettings

from app.core.pagination import normalise_paging



__all__ = ["SellingSettingsRepository"]





class SellingSettingsRepository:

    model = SellingSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[SellingSettings]:

        return db.scalar(

            select(SellingSettings).where(

                SellingSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: SellingSettings) -> SellingSettings:

        db.add(row)

        db.flush()

        return row
