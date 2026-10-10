"""Pydantic v2 schemas for ProductBundle."""





from __future__ import annotations

from typing import Optional

import uuid



from app.selling.product_bundle_item_domain.schemas.product_bundle_item import (

    ProductBundleItemCreate,

    ProductBundleItemRead,

)

from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ProductBundleCreate",

    "ProductBundleUpdate",

    "ProductBundleRead",

    "ProductBundleListResponse",

]





class ProductBundleBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    new_item_code_id: uuid.UUID

    description: Optional[str] = None

    is_active: Optional[bool] = None

    disabled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[ProductBundleItemCreate] = []





class ProductBundleCreate(ProductBundleBase):

    pass





class ProductBundleUpdate(InputSchema):

    """A partial update."""



    new_item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None

    disabled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: Optional[list[ProductBundleItemCreate]] = None





class ProductBundleRead(ReadSchema):

    id: uuid.UUID

    name: str

    new_item_code_id: Optional[uuid.UUID] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None

    disabled: Optional[bool] = None

    amended_from_id: Optional[uuid.UUID] = None

    items: list[ProductBundleItemRead] = []





ProductBundleListResponse = Page[ProductBundleRead]
