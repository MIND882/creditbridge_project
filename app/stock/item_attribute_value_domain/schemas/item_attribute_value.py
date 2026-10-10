"""Pydantic v2 schemas for ItemAttributeValue."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemAttributeValueCreate",

    "ItemAttributeValueRead",

    "ItemAttributeValueListResponse",

]





class ItemAttributeValueBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    attribute_value: str

    abbr: str





class ItemAttributeValueCreate(ItemAttributeValueBase):

    pass





class ItemAttributeValueUpdate(InputSchema):

    """A partial update."""



    attribute_value: Optional[str] = None

    abbr: Optional[str] = None





class ItemAttributeValueRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    attribute_value: str

    abbr: str





ItemAttributeValueListResponse = Page[ItemAttributeValueRead]
