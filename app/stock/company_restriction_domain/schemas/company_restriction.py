"""Pydantic v2 schemas for CompanyRestriction."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "CompanyRestrictionCreate",

    "CompanyRestrictionUpdate",

    "CompanyRestrictionRead",

    "CompanyRestrictionListResponse",

]





class CompanyRestrictionBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    company: str





class CompanyRestrictionCreate(CompanyRestrictionBase):

    pass





class CompanyRestrictionUpdate(InputSchema):

    """A partial update."""



    company: Optional[str] = None





class CompanyRestrictionRead(ReadSchema):

    id: uuid.UUID

    name: str

    company: str





CompanyRestrictionListResponse = Page[CompanyRestrictionRead]
