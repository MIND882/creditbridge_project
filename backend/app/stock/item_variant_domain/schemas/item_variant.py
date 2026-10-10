"""Pydantic v2 schemas for ItemVariant."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemVariantCreate",

    "ItemVariantUpdate",

    "ItemVariantRead",

    "ItemVariantListResponse",

]





class ItemVariantBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_attribute_id: uuid.UUID

    item_attribute_value: str





class ItemVariantCreate(ItemVariantBase):

    pass





class ItemVariantUpdate(InputSchema):

    """A partial update."""



    item_attribute_id: Optional[uuid.UUID] = None

    item_attribute_value: Optional[str] = None





class ItemVariantRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_attribute_id: Optional[uuid.UUID] = None

    item_attribute_value: str





ItemVariantListResponse = Page[ItemVariantRead]
