"""Pydantic v2 schemas for Brand."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "BrandCreate",

    "BrandUpdate",

    "BrandRead",

    "BrandListResponse",

]





class BrandBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    brand: str

    description: Optional[str] = None

    image: Optional[str] = None





class BrandCreate(BrandBase):

    pass





class BrandUpdate(InputSchema):

    """A partial update."""



    brand: Optional[str] = None

    description: Optional[str] = None

    image: Optional[str] = None





class BrandRead(ReadSchema):

    id: uuid.UUID

    name: str

    brand: str

    description: Optional[str] = None

    image: Optional[str] = None





BrandListResponse = Page[BrandRead]
