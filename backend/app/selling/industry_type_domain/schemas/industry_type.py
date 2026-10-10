"""Pydantic v2 schemas for IndustryType."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "IndustryTypeCreate",

    "IndustryTypeUpdate",

    "IndustryTypeRead",

    "IndustryTypeListResponse",

]





class IndustryTypeBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    industry: str





class IndustryTypeCreate(IndustryTypeBase):

    pass





class IndustryTypeUpdate(InputSchema):

    """A partial update."""



    industry: Optional[str] = None





class IndustryTypeRead(ReadSchema):

    id: uuid.UUID

    name: str

    industry: str





IndustryTypeListResponse = Page[IndustryTypeRead]
