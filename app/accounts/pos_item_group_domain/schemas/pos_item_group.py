"""Pydantic v2 schemas for POSItemGroup."""





from __future__ import annotations

from typing import Optional

import uuid



from app.core.base_schema import InputSchema, ReadSchema

from app.core.pagination import Page



__all__ = [

    "POSItemGroupCreate",

    "POSItemGroupRead",

    "POSItemGroupListResponse",

]





class POSItemGroupBase(InputSchema):

    """Client-supplied fields. Never accepts ``business_id``."""



    item_group: str





class POSItemGroupCreate(POSItemGroupBase):

    """Accepted only nested inside the parent payload."""

    pass





class POSItemGroupRead(ReadSchema):

    id: uuid.UUID

    idx: int

    parent_id: Optional[uuid.UUID] = None

    item_group: str





POSItemGroupListResponse = Page[POSItemGroupRead]
