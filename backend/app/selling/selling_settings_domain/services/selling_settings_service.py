"""Business logic for Selling Settings -- port of

``erpnext/selling/doctype/selling_settings/selling_settings.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.selling.selling_settings_domain.models.selling_settings import SellingSettings

from app.selling.selling_settings_domain.repositories.selling_settings_repository import (

    SellingSettingsRepository,

)

from app.selling.selling_settings_domain.schemas.selling_settings import (

    SellingSettingsUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["SellingSettingsService"]





class SellingSettingsService:

    def __init__(self, repository: Optional[SellingSettingsRepository] = None) -> None:

        self.repository = repository or SellingSettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> SellingSettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = SellingSettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: SellingSettingsUpdate

    ) -> SellingSettings:

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
