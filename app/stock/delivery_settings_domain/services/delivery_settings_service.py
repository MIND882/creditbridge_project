"""Business logic for Delivery Settings -- port of

``erpnext/stock/doctype/delivery_settings/delivery_settings.py``.



Upstream declares no validation, so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.delivery_settings_domain.models.delivery_settings import DeliverySettings

from app.stock.delivery_settings_domain.repositories.delivery_settings_repository import (

    DeliverySettingsRepository,

)

from app.stock.delivery_settings_domain.schemas.delivery_settings import (

    DeliverySettingsUpdate,

)

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["DeliverySettingsService"]





class DeliverySettingsService:

    def __init__(self, repository: Optional[DeliverySettingsRepository] = None) -> None:

        self.repository = repository or DeliverySettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> DeliverySettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = DeliverySettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: DeliverySettingsUpdate

    ) -> DeliverySettings:

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
