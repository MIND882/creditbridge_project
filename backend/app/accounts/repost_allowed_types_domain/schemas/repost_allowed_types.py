"""Pydantic v2 schemas for RepostAllowedTypes."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "RepostAllowedTypesCreate",

    "RepostAllowedTypesRead",

    "RepostAllowedTypesListResponse",

]





class RepostAllowedTypesBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    document_type: Optional[str] = None





class RepostAllowedTypesCreate(RepostAllowedTypesBase):

    """Accepted only nested inside the parent payload."""

    pass





class RepostAllowedTypesRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    document_type: Optional[str] = None





RepostAllowedTypesListResponse = Page[RepostAllowedTypesRead]
