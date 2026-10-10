"""Pydantic v2 schemas for ItemAlternative."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemAlternativeCreate",

    "ItemAlternativeUpdate",

    "ItemAlternativeRead",

    "ItemAlternativeListResponse",

]





class ItemAlternativeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    alternative_item_code_id: Optional[uuid.UUID] = None

    two_way: Optional[bool] = None

    item_name: Optional[str] = None

    alternative_item_name: Optional[str] = None





class ItemAlternativeCreate(ItemAlternativeBase):

    pass





class ItemAlternativeUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    alternative_item_code_id: Optional[uuid.UUID] = None

    two_way: Optional[bool] = None

    item_name: Optional[str] = None

    alternative_item_name: Optional[str] = None





class ItemAlternativeRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_code_id: Optional[uuid.UUID] = None

    alternative_item_code_id: Optional[uuid.UUID] = None

    two_way: Optional[bool] = None

    item_name: Optional[str] = None

    alternative_item_name: Optional[str] = None





ItemAlternativeListResponse = Page[ItemAlternativeRead]
