"""Pydantic v2 schemas for ItemManufacturer."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ItemManufacturerCreate",

    "ItemManufacturerUpdate",

    "ItemManufacturerRead",

    "ItemManufacturerListResponse",

]





class ItemManufacturerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    manufacturer_id: uuid.UUID

    manufacturer_part_no: str

    item_code_id: uuid.UUID

    item_name: Optional[str] = None

    description: Optional[str] = None

    is_default: Optional[bool] = None





class ItemManufacturerCreate(ItemManufacturerBase):

    pass





class ItemManufacturerUpdate(InputSchema):

    """A partial update."""



    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: Optional[str] = None

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    is_default: Optional[bool] = None





class ItemManufacturerRead(ReadSchema):

    id: uuid.UUID

    name: str

    manufacturer_id: Optional[uuid.UUID] = None

    manufacturer_part_no: str

    item_code_id: Optional[uuid.UUID] = None

    item_name: Optional[str] = None

    description: Optional[str] = None

    is_default: Optional[bool] = None





ItemManufacturerListResponse = Page[ItemManufacturerRead]
