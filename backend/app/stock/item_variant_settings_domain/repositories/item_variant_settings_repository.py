"""Data access for ItemVariantSettings. Scoped by ``business_id`` throughout."""



from __future__ import annotations



import uuid

from typing import Optional, Sequence



from sqlalchemy import func, select

from sqlalchemy.orm import Session



from app.stock.item_variant_settings_domain.models.item_variant_settings import ItemVariantSettings

from app.core.pagination import normalise_paging



__all__ = ["ItemVariantSettingsRepository"]





class ItemVariantSettingsRepository:

    model = ItemVariantSettings





    def get_for_business(

        self, db: Session, business_id: uuid.UUID

    ) -> Optional[ItemVariantSettings]:

        return db.scalar(

            select(ItemVariantSettings).where(

                ItemVariantSettings.business_id == business_id

            )

        )



    def add(self, db: Session, row: ItemVariantSettings) -> ItemVariantSettings:

        db.add(row)

        db.flush()

        return row
