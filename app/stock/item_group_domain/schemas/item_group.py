"""Pydantic v2 schemas for ItemGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemGroupCreate",

    "ItemGroupUpdate",

    "ItemGroupRead",

    "ItemGroupListResponse",

]





class ItemGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_group_name: str

    parent_item_group_id: Optional[uuid.UUID] = None

    is_group: Optional[bool] = None

    image: Optional[str] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None





class ItemGroupCreate(ItemGroupBase):

    pass





class ItemGroupUpdate(InputSchema):

    """A partial update."""



    item_group_name: Optional[str] = None

    parent_item_group_id: Optional[uuid.UUID] = None

    is_group: Optional[bool] = None

    image: Optional[str] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None





class ItemGroupRead(ReadSchema):

    id: uuid.UUID

    name: str

    item_group_name: str

    parent_item_group_id: Optional[uuid.UUID] = None

    is_group: Optional[bool] = None

    image: Optional[str] = None

    lft: Optional[int] = None

    rgt: Optional[int] = None

    old_parent_id: Optional[uuid.UUID] = None





ItemGroupListResponse = Page[ItemGroupRead]
