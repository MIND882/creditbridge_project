"""Pydantic v2 schemas for ItemWebsiteSpecification."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemWebsiteSpecificationCreate",

    "ItemWebsiteSpecificationUpdate",

    "ItemWebsiteSpecificationRead",

    "ItemWebsiteSpecificationListResponse",

]





class ItemWebsiteSpecificationBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    label: Optional[str] = None

    description: Optional[str] = None





class ItemWebsiteSpecificationCreate(ItemWebsiteSpecificationBase):

    pass





class ItemWebsiteSpecificationUpdate(InputSchema):

    """A partial update."""



    label: Optional[str] = None

    description: Optional[str] = None





class ItemWebsiteSpecificationRead(ReadSchema):

    id: uuid.UUID

    name: str

    label: Optional[str] = None

    description: Optional[str] = None





ItemWebsiteSpecificationListResponse = Page[ItemWebsiteSpecificationRead]
