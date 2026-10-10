"""Pydantic v2 schemas for VariantField."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "VariantFieldCreate",

    "VariantFieldRead",

    "VariantFieldListResponse",

]





class VariantFieldBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    field_name: str





class VariantFieldCreate(VariantFieldBase):

    pass





class VariantFieldUpdate(InputSchema):

    """A partial update."""



    field_name: Optional[str] = None





class VariantFieldRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    name: str

    field_name: str





VariantFieldListResponse = Page[VariantFieldRead]
