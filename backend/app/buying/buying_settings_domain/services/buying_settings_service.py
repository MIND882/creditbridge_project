"""Business logic for Buying Settings -- port of

``erpnext/buying/doctype/buying_settings/buying_settings.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.buying.buying_settings_domain.models.buying_settings import BuyingSettings

from app.buying.buying_settings_domain.repositories.buying_settings_repository import (

    BuyingSettingsRepository,

)

from app.buying.buying_settings_domain.schemas.buying_settings import (

    BuyingSettingsUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["BuyingSettingsService"]





class BuyingSettingsService:

    def __init__(self, repository: Optional[BuyingSettingsRepository] = None) -> None:

        self.repository = repository or BuyingSettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> BuyingSettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = BuyingSettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: BuyingSettingsUpdate

    ) -> BuyingSettings:

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
