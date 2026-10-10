"""Business logic for Item Variant Settings -- port of

``erpnext/stock/doctype/item_variant_settings/item_variant_settings.py``.



Upstream has 1 ``frappe.throw`` sites, all of them embedded in controller workflows that reach beyond field conversion (stock valuation, ledger writes, naming via ``frappe.naming``), so ``_validate`` is empty by design rather than by omission.

"""



from __future__ import annotations



import uuid

from typing import Optional



from sqlalchemy.orm import Session



from app.stock.item_variant_settings_domain.models.item_variant_settings import ItemVariantSettings

from app.stock.item_variant_settings_domain.repositories.item_variant_settings_repository import (

    ItemVariantSettingsRepository,

)

from app.stock.item_variant_settings_domain.schemas.item_variant_settings import (

    ItemVariantSettingsUpdate,

)

from app.stock.variant_field_domain.models.variant_field import VariantField

from app.core.errors import NotFoundError

from app.core.pagination import ResultPage



__all__ = ["ItemVariantSettingsService"]





class ItemVariantSettingsService:

    def __init__(self, repository: Optional[ItemVariantSettingsRepository] = None) -> None:

        self.repository = repository or ItemVariantSettingsRepository()





    def get_or_create(

        self, db: Session, business_id: uuid.UUID

    ) -> ItemVariantSettings:

        """The tenant's settings row, created with upstream defaults on first read."""

        row = self.repository.get_for_business(db, business_id)

        if row is None:

            row = ItemVariantSettings(business_id=business_id)

            try:

                self.repository.add(db, row)

                db.commit()

            except Exception:

                db.rollback()

                raise

            db.refresh(row)

        return row



    def update(

        self, db: Session, business_id: uuid.UUID, payload: ItemVariantSettingsUpdate

    ) -> ItemVariantSettings:

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
