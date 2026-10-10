"""Pydantic v2 schemas for Manufacturer."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "ManufacturerCreate",

    "ManufacturerUpdate",

    "ManufacturerRead",

    "ManufacturerListResponse",

]





class ManufacturerBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    short_name: str

    full_name: Optional[str] = None

    website: Optional[str] = None

    country: Optional[str] = None

    logo: Optional[str] = None

    notes: Optional[str] = None





class ManufacturerCreate(ManufacturerBase):

    pass





class ManufacturerUpdate(InputSchema):

    """A partial update."""



    short_name: Optional[str] = None

    full_name: Optional[str] = None

    website: Optional[str] = None

    country: Optional[str] = None

    logo: Optional[str] = None

    notes: Optional[str] = None





class ManufacturerRead(ReadSchema):

    id: uuid.UUID

    name: str

    short_name: str

    full_name: Optional[str] = None

    website: Optional[str] = None

    country: Optional[str] = None

    logo: Optional[str] = None

    notes: Optional[str] = None





ManufacturerListResponse = Page[ManufacturerRead]
