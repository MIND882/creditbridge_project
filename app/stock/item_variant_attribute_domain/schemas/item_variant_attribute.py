"""Pydantic v2 schemas for ItemVariantAttribute."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemVariantAttributeCreate",

    "ItemVariantAttributeRead",

    "ItemVariantAttributeListResponse",

]





class ItemVariantAttributeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    variant_of_id: Optional[uuid.UUID] = None

    attribute_id: uuid.UUID

    attribute_value: Optional[str] = None

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None





class ItemVariantAttributeCreate(ItemVariantAttributeBase):

    pass





class ItemVariantAttributeUpdate(InputSchema):

    """A partial update."""



    variant_of_id: Optional[uuid.UUID] = None

    attribute_id: Optional[uuid.UUID] = None

    attribute_value: Optional[str] = None

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None





class ItemVariantAttributeRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    variant_of_id: Optional[uuid.UUID] = None

    attribute_id: Optional[uuid.UUID] = None

    attribute_value: Optional[str] = None

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None





ItemVariantAttributeListResponse = Page[ItemVariantAttributeRead]
