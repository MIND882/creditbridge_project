"""Pydantic v2 schemas for UomCategory."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "UomCategoryCreate",

    "UomCategoryUpdate",

    "UomCategoryRead",

    "UomCategoryListResponse",

]





class UomCategoryBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    category_name: str





class UomCategoryCreate(UomCategoryBase):

    pass





class UomCategoryUpdate(InputSchema):

    """A partial update."""



    category_name: Optional[str] = None





class UomCategoryRead(ReadSchema):

    id: uuid.UUID

    name: str

    category_name: str





UomCategoryListResponse = Page[UomCategoryRead]
