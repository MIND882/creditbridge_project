"""Pydantic v2 schemas for POSProfileUser."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSProfileUserCreate",

    "POSProfileUserRead",

    "POSProfileUserListResponse",

]





class POSProfileUserBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    default: Optional[bool] = None

    user: Optional[str] = None





class POSProfileUserCreate(POSProfileUserBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSProfileUserRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    default: bool

    user: Optional[str] = None





POSProfileUserListResponse = Page[POSProfileUserRead]
