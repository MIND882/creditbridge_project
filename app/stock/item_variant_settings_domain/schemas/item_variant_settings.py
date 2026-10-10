"""Pydantic v2 schemas for ItemVariantSettings."""





from __future__ import annotations

from typing import Optional

import uuid



from app.stock.variant_field_domain.schemas.variant_field import (

    VariantFieldCreate,

    VariantFieldRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemVariantSettingsUpdate",

    "ItemVariantSettingsRead",

]





class ItemVariantSettingsUpdate(InputSchema):

    """A partial update of the tenant settings row."""



    do_not_update_variants: Optional[bool] = None

    allow_rename_attribute_value: Optional[bool] = None

    allow_different_uom: Optional[bool] = None





class ItemVariantSettingsRead(ReadSchema):

    id: uuid.UUID

    do_not_update_variants: Optional[bool] = None

    allow_rename_attribute_value: Optional[bool] = None

    allow_different_uom: Optional[bool] = None

    fields: list[VariantFieldRead] = []


