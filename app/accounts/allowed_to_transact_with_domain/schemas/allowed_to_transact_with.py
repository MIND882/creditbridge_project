"""Pydantic v2 schemas for AllowedToTransactWith."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "AllowedToTransactWithCreate",

    "AllowedToTransactWithRead",

    "AllowedToTransactWithListResponse",

]





class AllowedToTransactWithBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    pass





class AllowedToTransactWithCreate(AllowedToTransactWithBase):

    """Accepted only nested inside the parent payload."""

    pass





class AllowedToTransactWithRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None





AllowedToTransactWithListResponse = Page[AllowedToTransactWithRead]
