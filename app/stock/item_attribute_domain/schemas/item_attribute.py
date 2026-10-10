"""Pydantic v2 schemas for ItemAttribute."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.stock.item_attribute_value_domain.schemas.item_attribute_value import (

    ItemAttributeValueCreate,

    ItemAttributeValueRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemAttributeCreate",

    "ItemAttributeUpdate",

    "ItemAttributeRead",

    "ItemAttributeListResponse",

]





class ItemAttributeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    attribute_name: str

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None

    item_attribute_values: list[ItemAttributeValueCreate] = []





class ItemAttributeCreate(ItemAttributeBase):

    pass





class ItemAttributeUpdate(InputSchema):

    """A partial update."""



    attribute_name: Optional[str] = None

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None

    item_attribute_values: Optional[list[ItemAttributeValueCreate]] = None





class ItemAttributeRead(ReadSchema):

    id: uuid.UUID

    name: str

    attribute_name: str

    numeric_values: Optional[bool] = None

    from_range: Optional[Decimal] = None

    increment: Optional[Decimal] = None

    to_range: Optional[Decimal] = None

    disabled: Optional[bool] = None

    item_attribute_values: list[ItemAttributeValueRead] = []





ItemAttributeListResponse = Page[ItemAttributeRead]
