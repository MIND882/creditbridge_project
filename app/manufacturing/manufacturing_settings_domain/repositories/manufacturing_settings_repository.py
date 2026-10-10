"""Data access for ManufacturingSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.manufacturing.manufacturing_settings_domain.models.manufacturing_settings import ManufacturingSettings

from app.core.pagination import normalise_paging



__all__ = ["ManufacturingSettingsRepository"]





class ManufacturingSettingsRepository:

    model = ManufacturingSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[ManufacturingSettings]:

        return db.scalar(

            select(ManufacturingSettings).where(

                ManufacturingSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: ManufacturingSettings) -> ManufacturingSettings:

        db.add(row)

        db.flush()

        return row
