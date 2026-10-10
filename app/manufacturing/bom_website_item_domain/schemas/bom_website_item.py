"""Pydantic v2 schemas for BomWebsiteItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BomWebsiteItemCreate",

    "BomWebsiteItemRead",

    "BomWebsiteItemListResponse",

]





class BomWebsiteItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    website_image: Optional[str] = None





class BomWebsiteItemCreate(BomWebsiteItemBase):

    pass





class BomWebsiteItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    website_image: Optional[str] = None





class BomWebsiteItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    qty: Optional[Decimal] = None

    website_image: Optional[str] = None





BomWebsiteItemListResponse = Page[BomWebsiteItemRead]
