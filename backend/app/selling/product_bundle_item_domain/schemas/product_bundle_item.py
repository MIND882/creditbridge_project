"""Pydantic v2 schemas for ProductBundleItem."""





from __future__ import annotations

from decimal import Decimal

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductBundleItemCreate",

    "ProductBundleItemRead",

    "ProductBundleItemListResponse",

]





class ProductBundleItemBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_code_id: uuid.UUID

    qty: Decimal

    description: Optional[str] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None





class ProductBundleItemCreate(ProductBundleItemBase):

    pass





class ProductBundleItemUpdate(InputSchema):

    """A partial update."""



    item_code_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    description: Optional[str] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None





class ProductBundleItemRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    item_code_id: Optional[uuid.UUID] = None

    qty: Optional[Decimal] = None

    description: Optional[str] = None

    rate: Optional[Decimal] = None

    uom_id: Optional[uuid.UUID] = None





ProductBundleItemListResponse = Page[ProductBundleItemRead]
