"""Business logic for Manufacturing Settings -- port of

``erpnext/manufacturing/doctype/manufacturing_settings/manufacturing_settings.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.manufacturing.manufacturing_settings_domain.models.manufacturing_settings import ManufacturingSettings

from app.manufacturing.manufacturing_settings_domain.repositories.manufacturing_settings_repository import (

    ManufacturingSettingsRepository,

)

from app.manufacturing.manufacturing_settings_domain.schemas.manufacturing_settings import (

    ManufacturingSettingsUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ManufacturingSettingsService"]





class ManufacturingSettingsService:

    def __init__(self, repository: Optional[ManufacturingSettingsRepository] = None) -> None:

        self.repository = repository or ManufacturingSettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> ManufacturingSettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = ManufacturingSettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: ManufacturingSettingsUpdate

    ) -> ManufacturingSettings:

        row = self.get_or_create(db, business_id)

        changes = payload.model_dump(exclude_unset=True)

        if not changes:

            return row

        try:

            for field_name, value in changes.items():

                setattr(row, field_name, value)

            db.flush()

        except Exception:

            db.rollback()

            raise

        db.commit()

        db.refresh(row)

        return row
